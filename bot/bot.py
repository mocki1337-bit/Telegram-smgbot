import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

if not TOKEN:
    raise Exception(" тоен не установлен")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_btn = telebot.types.KeyboardButton(
        " Открыть приложение",
        web_app=telebot.types.WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_btn)

    bot.send_message(
        message.chat.id,
        " Бот запущен!\n\nНажми кнопку ниже:",
        reply_markup=markup
    )

print(" Bot started...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
