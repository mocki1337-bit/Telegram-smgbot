import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, jsonify, send_from_directory
import json
import requests
import threading
import os


TELEGRAM_TOKEN = os.environ.get(
    "TELEGRAM_TOKEN", "8436030211:AAEN91cJvS3xl1H3_2ApiLwZCXLKkPxcYoY"
)
GROQ_API_KEY = os.environ.get(
    "GROQ_API_KEY", "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"
)
RENDER_URL = os.environ.get(
    "RENDER_URL", "https://telegram-smgbot.onrender.com"
)  
app = Flask(__name__, static_folder="../frontend")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Загрузка исторических данных
try:
    with open("historical_texts.json", "r", encoding="utf-8") as f:
        historical_data = json.load(f)
except FileNotFoundError:
    print("historical_texts.json не найден, используем дефолтные данные")
    historical_data = []

user_context = {}


def get_character_context(character):
    """Получение контекста персонажа"""
    for char_data in historical_data:
        if char_data["character"] == character:
            return (
                char_data["context"],
                char_data["speech_style"],
                char_data["historical_texts"],
            )

    # Дефолтные персонажи
    contexts = {
        "soldier": (
            "Солдат в окопах под Сморгони",
            "простой, грубоватый",
            ["В окопах по пояс в воде", "Немцы стреляют"],
        ),
        "nurse": (
            "Медсестра в полевом госпитале",
            "заботливый, мягкий",
            ["Раненых много", "Перевязываю всю ночь"],
        ),
        "resident": (
            "Житель Сморгони",
            "испуганный, усталый",
            ["Немцы близко", "Хлеб кончился"],
        ),
    }
    return contexts.get(character, ("Персонаж не найден.", None, None))


def generate_response(character, user_message):
    """Генерация ответа через Groq AI"""
    context, speech_style, texts = get_character_context(character)
    if context.startswith("Персонаж"):
        return context

    prompt = f"""Ты {character} из Сморгони, 1916 год.
Стиль: {speech_style}
Контекст: {context}

Вопрос: "{user_message}"

Ответь КРАТКО (2-3 предложения) + факт о Сморгони 1916."""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 250,
                "temperature": 0.8,
            },
            timeout=10,
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Ошибка Groq API: {e}")
        return f"{character}: Не могу ответить сейчас..."


# Flask routes
@app.route("/")
def index():
    """Главная страница - отдаём frontend"""
    return send_from_directory("../frontend", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat_api():
    """API для чата"""
    data = request.json
    character = data.get("character", "soldier")
    message = data.get("message", "")
    response = generate_response(character, message)
    return jsonify({"response": response})


@app.route("/health")
def health():
    """Health check для Render"""
    return jsonify({"status": "ok"})


# Telegram bot handlers
@bot.message_handler(commands=["start"])
def start(message):
    """Стартовое сообщение"""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "🎮 Приложение", web_app=telebot.types.WebAppInfo(url=RENDER_URL)
        )
    )

    bot.send_message(
        message.chat.id,
        "👋 Привет! Добро пожаловать!\n\n"
        "Нажми на кнопку ниже чтобы открыть приложение:",
        reply_markup=markup,
    )


def run_bot():
    """Запуск бота"""
    print("🤖 Telegram бот запущен!")
    bot.infinity_polling(none_stop=True)


def run_flask():
    """Запуск Flask сервера"""
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Flask запущен на порту {port}")
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    print("=== СМОРГОНЬ 1916 ===")
    print(f"Render URL: {RENDER_URL}")

    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Запускаем Flask в основном потоке
    run_flask()
