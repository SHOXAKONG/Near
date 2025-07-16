import requests
import pandas as pd
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth
from django.http import JsonResponse
from django.shortcuts import render
from asgiref.sync import sync_to_async
from decouple import config
from src.apps.history.models import SearchHistory
from src.apps.users.models import Users

BASE_URL = config('BASE_URL')


# ✨ CORRECTED AND UPDATED VIEW
async def api_users_list(request):
    try:
        # --- Get query parameters ---
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)
        role_filter = request.GET.get('role', '')
        sort_by_name = request.GET.get('sort_by_name', 'asc') # Default to ascending

        # --- Base queryset ---
        base_query = Users.objects.all()

        # --- Apply role filter if provided ---
        if role_filter:
            base_query = base_query.filter(role=role_filter)

        # --- Apply sorting by name ---
        sort_order = '' if sort_by_name == 'asc' else '-'
        base_query = base_query.order_by(f'{sort_order}first_name', f'{sort_order}last_name')

        # --- Fetch data from database ---
        users_from_db = await sync_to_async(list)(
            base_query.values('id', 'first_name', 'last_name', 'role', 'is_active')
        )

        # --- Process data in Python ---
        processed_users = [
            {
                'id': user['id'],
                'full_name': f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
                'role': user['role'],
                'is_active': user['is_active']
            }
            for user in users_from_db
        ]

        # --- Paginate the results ---
        paginator = Paginator(processed_users, page_size)
        page_obj = paginator.get_page(page_number)

        # --- Build pagination links that preserve filters ---
        query_params = f"role={role_filter}&sort_by_name={sort_by_name}&page_size={page_size}"
        next_link = f'{BASE_URL}/uz/dashboard/api/users-list/?{query_params}&page={page_obj.next_page_number()}' if page_obj.has_next() else None
        prev_link = f'{BASE_URL}/uz/dashboard/api/users-list/?{query_params}&page={page_obj.previous_page_number()}' if page_obj.has_previous() else None

        # --- Prepare final JSON response ---
        data = {
            'count': paginator.count,
            'next': next_link,
            'previous': prev_link,
            'results': list(page_obj.object_list)
        }
        return JsonResponse(data)

    except Exception as e:
        print(f"!!! Error in api_users_list: {e}")
        return JsonResponse({'error': str(e)}, status=500)


async def main_dashboard_view(request):
    # Pass unique roles to the template for the filter dropdown
    roles = await sync_to_async(list)(Users.objects.values_list('role', flat=True).distinct())
    return render(request, 'dashboard/main_dashboard.html', {'roles': roles})


# ... the rest of your views.py file ...
async def api_active_users_data(request):
    api_url = f"{BASE_URL}/api/statistics/active-users/"
    try:
        data = await sync_to_async(requests.get)(api_url, timeout=10)
        data.raise_for_status()

        df = pd.DataFrame(data.json()).head(10)

        chart_data = {
            'labels': df['first_name'].tolist(),
            'datasets': [{
                'label': 'Jami Qidiruvlar Soni',
                'data': df['total_searches'].tolist(),
                'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        }
        return JsonResponse(chart_data)

    except Exception as e:
        print(f"Error in api_active_users_data: {e}")
        return JsonResponse({'error': str(e)}, status=500)


async def api_category_pie_data(request):
    api_url = f"{BASE_URL}/api/statistics/search-history/"
    try:
        data = await sync_to_async(requests.get)(api_url, timeout=10)
        data.raise_for_status()
        df = pd.DataFrame(data.json()).head(5)

        chart_data = {
            'labels': df['category_name'].tolist(),
            'datasets': [{
                'data': df['search_count'].tolist(),
                'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
            }]
        }
        return JsonResponse(chart_data)
    except Exception as e:
        print(f"Error in api_category_pie_data: {e}")
        return JsonResponse({'error': str(e)}, status=500)


async def api_daily_search_stats(request):
    try:
        queryset = await sync_to_async(list)(
            SearchHistory.objects.annotate(
                date=TruncDate('created_at')
            ).values('date')
            .annotate(search_count=Count('id'))
            .order_by('date')
        )

        if not queryset:
            return JsonResponse({'labels': [], 'datasets': []})

        df = pd.DataFrame(queryset)

        df['date'] = pd.to_datetime(df['date'])

        chart_data = {
            'labels': df['date'].dt.strftime('%Y-%m-%d').tolist(),
            'datasets': [{
                'label': 'Kunlik Qidiruvlar Soni',
                'data': df['search_count'].tolist(),
                'fill': True,
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'tension': 0.1
            }]
        }
        return JsonResponse(chart_data)

    except Exception as e:
        print(f"!!! Error in api_daily_search_stats: {e}")
        return JsonResponse({'error': str(e)}, status=500)


async def api_monthly_stats_data(request):
    try:
        user_stats = await sync_to_async(list)(
            Users.objects.annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(user_registrations=Count('id'))
            .order_by('month')
        )

        search_stats = await sync_to_async(list)(
            SearchHistory.objects.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(category_searches=Count('id'))
            .order_by('month')
        )

        users_df = pd.DataFrame(user_stats)
        searches_df = pd.DataFrame(search_stats)

        if not users_df.empty:
            users_df['month'] = pd.to_datetime(users_df['month'])
        if not searches_df.empty:
            searches_df['month'] = pd.to_datetime(searches_df['month'])

        if not users_df.empty and not searches_df.empty:
            merged_df = pd.merge(users_df, searches_df, on='month', how='outer').fillna(0)
        elif not users_df.empty:
            merged_df = users_df.fillna(0)
        elif not searches_df.empty:
            merged_df = searches_df.fillna(0)
        else:
            return JsonResponse({'labels': [], 'datasets': []})

        chart_data = {
            'labels': merged_df['month'].dt.strftime('%b %Y').tolist(),
            'datasets': [
                {
                    'label': 'Yangi Foydalanuvchilar',
                    'data': merged_df['user_registrations'].tolist(),
                    'backgroundColor': 'rgba(54, 162, 235, 0.7)',
                },
                {
                    'label': 'Qidiruvlar Soni',
                    'data': merged_df['category_searches'].tolist(),
                    'backgroundColor': 'rgba(75, 192, 192, 0.7)',
                }
            ]
        }
        return JsonResponse(chart_data)

    except Exception as e:
        print(f"!!! Error in api_monthly_stats_data: {e}")
        return JsonResponse({'error': str(e)}, status=500)