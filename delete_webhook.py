from decouple import config
import telebot

BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

try:
    bot.delete_webhook()
    print("Webhook has been deleted successfully.")
except Exception as e:
    print(f"An error occurred: {e}")