from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import telebot
import json
from . import bot_logic

bot = telebot.TeleBot(settings.BOT_TOKEN, threaded=False)


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_string)

        if update.message:
            bot_logic.text_handler(update.message, bot)
        elif update.callback_query:
            bot_logic.callback_query_handler(update.callback_query, bot)

        return HttpResponse(status=200)
    return HttpResponse('Webhook endpoint')

