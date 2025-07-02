import telebot
from decouple import config

TOKEN = config('BOT_TOKEN')
WEBHOOK_URL = config('WEBHOOK_URL')

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()
bot.set_webhook(WEBHOOK_URL)

print("Webhook set!")
