import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings
from .utils import convert_image


def refresh_access_token(profile):
    if not profile.refresh_token:
        return None

    url = f"{settings.BASE_URL}/{profile.language}/api/auth/token/refresh/"
    try:
        response = requests.post(url, json={'refresh': profile.refresh_token})
        if response.status_code == 200:
            new_access_token = response.json().get('access')
            profile.access_token = new_access_token
            profile.save(update_fields=['access_token'])
            return new_access_token
        else:
            profile.user = None
            profile.access_token = None
            profile.refresh_token = None
            profile.save()
            return None
    except requests.RequestException:
        return None


def make_authenticated_request(profile, method, url, **kwargs):
    if not profile.access_token:
        print("Error: No access token found for authenticated request.")
        return None

    headers = kwargs.setdefault('headers', {})
    headers['Authorization'] = f'Bearer {profile.access_token}'

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.request(method, url, **kwargs)

    if response.status_code == 401:
        new_token = refresh_access_token(profile)
        if new_token:
            headers['Authorization'] = f'Bearer {new_token}'
            response = session.request(method, url, **kwargs)
        else:
            print("Failed to refresh token.")

    return response


def add_place(profile, place_data: dict):
    url = f"{settings.BASE_URL}/{profile.language}/api/place/"

    image_path = place_data.pop('image_path', None)
    files_to_upload = {}
    file_handle = None

    try:
        if image_path and os.path.exists(image_path):
            file_handle = open(image_path, 'rb')
            image_name = os.path.basename(image_path)
            files_to_upload['image'] = (image_name, file_handle, 'image/jpeg')

        response = make_authenticated_request(profile, 'post', url, data=place_data, files=files_to_upload, timeout=25)
        return response

    except requests.RequestException as e:
        return None
    finally:
        if file_handle:
            file_handle.close()
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"Temporary file {image_path} deleted.")
            except OSError as e:
                print(f"Error deleting temporary file {image_path}: {e}")



def register_user(lang: str, data: dict):
    url = f"{settings.BASE_URL}/{lang}/api/auth/register/"
    return requests.post(url, json=data)


def login_with_password(lang: str, email: str, password: str):
    url = f"{settings.BASE_URL}/{lang}/api/auth/login/"
    return requests.post(url, json={"email": email, "password": password})


def get_user_data_from_api(profile):
    if not profile.user:
        return None
    user_id = profile.user.id
    url = f"{settings.BASE_URL}/{profile.language}/api/auth/users-data/{user_id}/"
    return make_authenticated_request(profile, 'get', url)


def get_categories(profile):
    url = f"{settings.BASE_URL}/{profile.language}/api/category/"
    try:
        return requests.get(url, timeout=10)
    except requests.RequestException as e:
        print(f"Error fetching categories: {e}")
        return None


def search_places(profile, lat: float, lon: float, category_id: int):
    url = f"{settings.BASE_URL}/{profile.language}/api/place/"
    params = {'latitude': lat, 'longitude': lon, 'category': category_id}
    try:
        return requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        print(f"Error searching places: {e}")
        return None


def log_search_activity(profile, category_id: int):
    if not profile.user:
        return
    url = f"{settings.BASE_URL}/{profile.language}/api/search-history/"
    data = {'category': category_id}
    return make_authenticated_request(profile, 'post', url, json=data)


def confirm_registration(lang: str, code: str):
    url = f"{settings.BASE_URL}/{lang}/api/auth/confirm/"
    return requests.post(url, json={"code": code})


def become_entrepreneur(profile):
    url = f"{settings.BASE_URL}/{profile.language}/api/auth/become-entrepreneur/"
    return make_authenticated_request(profile, 'post', url)

def forgot_password(lang: str, email: str):
    url = f"{settings.BASE_URL}/{lang}/api/auth/forgot_password/"
    return requests.post(url, json={'email': email})


def restore_password(lang: str, data: dict):
    url = f"{settings.BASE_URL}/{lang}/api/auth/restore_password/"
    return requests.post(url, json=data)