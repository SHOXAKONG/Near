from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .telegram_bot import bot
import telebot

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return HttpResponse("OK", status=200)
    return HttpResponse("Unsupported method", status=405)
