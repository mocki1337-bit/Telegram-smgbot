import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv(
    "WEBAPP_URL", "https://telegram-smgbot.onrender.com"
)  # поменяй на свой URL

if not TOKEN:
    print("❌ BOT_TOKEN не установлен в переменных окружения")
    raise SystemExit(1)

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=["start", "help"])
def cmd_start(message: types.Message):
    # 1) Inline кнопка с обычным URL (откроется в браузере)
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(
        types.InlineKeyboardButton(text="Открыть сайт (в браузере)", url=WEBAPP_URL)
    )

    # 2) ReplyKeyboard с WebApp кнопкой (открывает Web App внутри Telegram и передаёт initData)
    try:
        webapp = types.WebAppInfo(url=WEBAPP_URL)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton(text="Открыть Web App (Telegram)", web_app=webapp)
        )
    except Exception:
        # На старых версиях библиотеки/клиента WebAppInfo может не работать — тогда просто не добавляем
        keyboard = None

    bot.send_message(
        message.chat.id,
        "Привет! Можешь открыть сайт в браузере или открыть Web App прямо в Telegram (если клиент поддерживает):",
        reply_markup=inline_kb,
    )

    if keyboard:
        bot.send_message(
            message.chat.id,
            "Или попробуй Web App (внутри Telegram):",
            reply_markup=keyboard,
        )


@bot.message_handler(func=lambda m: True)
def echo_all(message: types.Message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")


if __name__ == "__main__":
    print("✅ Bot started. Waiting for messages...")
    # infinity_polling() безопасно запускает polling и перезапускает при ошибках
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
