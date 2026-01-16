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
    print("🌐 Keep-alive сервер запущен")import os
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ========== ВАШ ТОКЕН ==========
BOT_TOKEN = "8523036017:AAEpFT_A9SawjpGvJ6ef391FMYJK5h4mmm"  # Пока оставьте так, потом поменяем

# ========== ОСТАЛЬНОЙ ВАШ КОД ==========
# Вставьте ВЕСЬ ваш код из bot_priceoriginal.py
# начиная от import и до самого конца

# Только добавьте в САМЫЙ КОНЕЦ вместо if __name__ == '__main__':
# вот это:
if __name__ == '__main__':
    print("🤖 Запуск бота...")
    
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики (те же что у вас)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот готов к работе!")
    application.run_polling()
