"""
Этот файл поддерживает работу бота 24/7
Добавьте эти строки в НАЧАЛО вашего bot.py:

from keep_alive import keep_alive
keep_alive()
"""

from flask import Flask
from threading import Thread
import time

app = Flask('')

@app.route('/')
def home():
    return "🤖 Telegram Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Запускает веб-сервер в фоне"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("🌐 Keep-alive сервер запущен")
