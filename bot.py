import os
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ========== ДЛЯ РАБОТЫ 24/7 ==========
from keep_alive import keep_alive
keep_alive()

# ========== НАСТРОЙКА ==========
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8523036017:AAEpFT_A9SawjpGv")

# Данные
PRICES = {
    "accessories": {"🕶 Очки": "10,000$"},
    "cars": {"🚗 ВАЗ": "50,000 ₽"}
}
ADMIN_LIST = ["egrixxx"]

# ========== КОМАНДЫ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🏠 Имущество", callback_data='property')]]
    await update.message.reply_text("👋 Привет!", reply_markup=InlineKeyboardMarkup(keyboard))

async def property_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🕶 Аксессуары", callback_data='accessories')],
        [InlineKeyboardButton("🚗 Автомобили", callback_data='cars')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='main')]
    ]
    
    # ЗДЕСЬ БЫЛА ОШИБКА - ТЕПЕРЬ ИСПРАВЛЕНО!
    await query.edit_message_text(
        "🏠 Имущество:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    text = f"📊 {data}:\n\n"
    
    for item, price in PRICES.get(data, {}).items():
        text += f"• {item}: {price}\n"
    
    # ЕЩЕ ОДНО ИСПРАВЛЕНИЕ!
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data='property')]])
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'main':
        await start(update, context)
    elif data == 'property':
        await property_menu(update, context)
    elif data in ['accessories', 'cars']:
        await show_category(update, context)

# ========== ЗАПУСК ==========
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()def save_data(prices):
    """Сохраняет данные в файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)

def save_admins(admins):
    """Сохраняет список админов"""
    with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
        json.dump(admins, f, ensure_ascii=False, indent=2)

# Загружаем данные
PRICES, ADMIN_LIST = load_data()

# ========== ПРОВЕРКА АДМИНА ==========
def is_admin(username):
    """Проверяет, является ли пользователь админом"""
    return username.lower() in ADMIN_LIST

# ========== ОСНОВНЫЕ КОМАНДЫ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню"""
    user = update.effective_user
    username = user.username
    
    keyboard = [
        [InlineKeyboardButton("🏠 Имущество", callback_data='property')],
        [InlineKeyboardButton("❓ Помощь", callback_data='help')],
        [InlineKeyboardButton("💡 Предложить цену", callback_data='suggest')]
    ]
    
    # Кнопка админ-панели для админов
    if username and is_admin(username):
        keyboard.append([InlineKeyboardButton("⚙️ Админ-панель", callback_data='admin_panel')])
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "🎯 <b>СРЕДНИЕ ЦЕНЫ BLACK RUSSIA</b>\n"
        "Сервер: Arzamas (33)\n\n"
        "Выберите категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /admin для админов"""
    user = update.effective_user
    username = user.username
    
    if not username or not is_admin(username):
        await update.message.reply_text("❌ У вас нет доступа к админ-панели!")
        return
    
    await show_admin_panel(update, context)

# ========== АДМИН-ПАНЕЛЬ ==========
async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает админ-панель"""
    keyboard = [
        [InlineKeyboardButton("📝 Изменить цены", callback_data='admin_edit')],
        [InlineKeyboardButton("👥 Управление админами", callback_data='admin_manage')],
        [InlineKeyboardButton("📊 Статистика", callback_data='admin_stats')],
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data='main')]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "⚙️ <b>АДМИН-ПАНЕЛЬ</b>\n\n"
            "Выберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            "⚙️ <b>АДМИН-ПАНЕЛЬ</b>\n\n"
            "Выберите действие:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

# ========== РЕДАКТИРОВАНИЕ ЦЕН ==========
async def admin_edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню редактирования цен"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🕶 Аксессуары", callback_data='edit_accessories')],
        [InlineKeyboardButton("🚗 Автомобили", callback_data='edit_cars')],
        [InlineKeyboardButton("🎨 Скины", callback_data='edit_skins')],
        [InlineKeyboardButton("🏡 Дома", callback_data='edit_houses')],
        [InlineKeyboardButton("➕ Добавить позицию", callback_data='add_item_menu')],
        [InlineKeyboardButton("⬅️ Назад в админку", callback_data='admin_panel')]
    ]
    
    await query.edit_message_text(
        "📝 <b>Редактирование цен</b>\n\n"
        "Выберите категорию для редактирования:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def edit_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Показывает список позиций в категории"""
    query = update.callback_query
    await query.answer()
    
    category_names = {
        'accessories': 'Аксессуары',
        'cars': 'Автомобили',
        'skins': 'Скины',
        'houses': 'Дома'
    }
    
    keyboard = []
    for item in PRICES[category]:
        btn_text = f"✏️ {item}: {PRICES[category][item]}"
        # Заменяем пробелы на _ в названии для callback
        item_safe = item.replace(' ', '_')
        callback_data = f"edit_{category}_{item_safe}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])
    
    keyboard.append([InlineKeyboardButton("➕ Добавить в эту категорию", 
                                         callback_data=f'add_to_{category}')])
    keyboard.append([InlineKeyboardButton("⬅️ Назад к редактированию", 
                                         callback_data='admin_edit')])
    
    await query.edit_message_text(
        f"📝 <b>Редактирование: {category_names[category]}</b>\n\n"
        "Нажмите на позицию для редактирования:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def edit_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начинает редактирование позиции"""
    query = update.callback_query
    await query.answer()
    
    data = query.data  # edit_cars_ВАЗ-2106
    parts = data.split('_')
    category = parts[1]
    item_name = '_'.join(parts[2:])  # Восстанавливаем оригинальное имя
    item_name = item_name.replace('_', ' ')  # Заменяем _ обратно на пробелы
    
    # Сохраняем данные для следующего сообщения
    context.user_data['editing'] = {'category': category, 'item': item_name}
    
    current_price = PRICES[category][item_name]
    
    await query.edit_message_text(
        f"✏️ <b>Редактирование:</b> {item_name}\n"
        f"📊 <b>Текущая цена:</b> {current_price}\n\n"
        "Отправьте новую цену в следующем сообщении.\n"
        "Пример: 50,000 - 70,000 ₽\n\n"
        "❌ Чтобы отменить, отправьте /cancel",
        parse_mode='HTML'
    )

async def add_item_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню добавления новой позиции"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🕶 В аксессуары", callback_data='add_accessories')],
        [InlineKeyboardButton("🚗 В автомобили", callback_data='add_cars')],
        [InlineKeyboardButton("🎨 В скины", callback_data='add_skins')],
        [InlineKeyboardButton("🏡 В дома", callback_data='add_houses')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='admin_edit')]
    ]
    
    await query.edit_message_text(
        "➕ <b>Добавление новой позиции</b>\n\n"
        "Выберите категорию:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def add_item_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Запрос названия для новой позиции"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['adding'] = {'category': category, 'step': 'name'}
    
    category_name = {
        'accessories': 'аксессуары',
        'cars': 'автомобили',
        'skins': 'скины',
        'houses': 'дома'
    }.get(category, category)
    
    await query.edit_message_text(
        f"➕ <b>Добавление в {category_name}</b>\n\n"
        "Отправьте название новой позиции.\n"
        "Пример: BMW X5\n\n"
        "❌ Чтобы отменить, отправьте /cancel",
        parse_mode='HTML'
    )

# ========== УПРАВЛЕНИЕ АДМИНАМИ ==========
async def admin_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление списком админов"""
    query = update.callback_query
    await query.answer()
    
    admins_list = "\n".join([f"• @{admin}" for admin in ADMIN_LIST])
    
    keyboard = [
        [InlineKeyboardButton("➕ Добавить админа", callback_data='add_admin')],
        [InlineKeyboardButton("➖ Удалить админа", callback_data='remove_admin')],
        [InlineKeyboardButton("⬅️ Назад в админку", callback_data='admin_panel')]
    ]
    
    await query.edit_message_text(
        "👥 <b>Управление администраторами</b>\n\n"
        f"<b>Текущие админы ({len(ADMIN_LIST)}):</b>\n{admins_list}\n\n"
        "Добавить можно только по username (без @)",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def add_admin_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос username нового админа"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['admin_action'] = 'add'
    
    await query.edit_message_text(
        "➕ <b>Добавление администратора</b>\n\n"
        "Отправьте username нового админа (без @).\n"
        "Пример: username123\n\n"
        "❌ Чтобы отменить, отправьте /cancel",
        parse_mode='HTML'
    )

async def remove_admin_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос username админа для удаления"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['admin_action'] = 'remove'
    
    admins_list = "\n".join([f"• @{admin}" for admin in ADMIN_LIST])
    
    await query.edit_message_text(
        "➖ <b>Удаление администратора</b>\n\n"
        f"<b>Текущие админы:</b>\n{admins_list}\n\n"
        "Отправьте username админа для удаления (без @).\n"
        "Пример: username123\n\n"
        "❌ Чтобы отменить, отправьте /cancel",
        parse_mode='HTML'
    )

# ========== СТАТИСТИКА ==========
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает статистику бота"""
    query = update.callback_query
    await query.answer()
    
    total_items = sum(len(items) for items in PRICES.values())
    
    stats_text = (
        f"📊 <b>СТАТИСТИКА БОТА</b>\n\n"
        f"📁 <b>Категории:</b> {len(PRICES)}\n"
        f"📦 <b>Всего позиций:</b> {total_items}\n"
        f"👥 <b>Администраторов:</b> {len(ADMIN_LIST)}\n\n"
        f"<b>По категориям:</b>\n"
    )
    
    for category, items in PRICES.items():
        category_name = {
            'accessories': 'Аксессуары',
            'cars': 'Автомобили',
            'skins': 'Скины',
            'houses': 'Дома'
        }.get(category, category)
        
        stats_text += f"• {category_name}: {len(items)} позиций\n"
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад в админку", callback_data='admin_panel')]]
    
    await query.edit_message_text(
        stats_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

# ========== ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает текстовые сообщения (для редактирования)"""
    message_text = update.message.text.strip()
    user = update.effective_user
    username = user.username
    
    # Проверка прав админа
    if not username or not is_admin(username):
        return
    
    user_data = context.user_data
    
    # Отмена действий
    if message_text.lower() == '/cancel':
        user_data.clear()
        await update.message.reply_text("❌ Действие отменено.")
        await show_admin_panel(update, context)
        return
    
    # Добавление/удаление админа
    if 'admin_action' in user_data:
        action = user_data['admin_action']
        new_admin = message_text.lower().strip()
        
        if action == 'add':
            if new_admin in ADMIN_LIST:
                await update.message.reply_text(f"❌ @{new_admin} уже является админом!")
            else:
                ADMIN_LIST.append(new_admin)
                save_admins(ADMIN_LIST)
                await update.message.reply_text(f"✅ @{new_admin} добавлен в список админов!")
        elif action == 'remove':
            if new_admin in ADMIN_LIST:
                if new_admin == DEFAULT_ADMINS[0]:  # Защита главного админа
                    await update.message.reply_text("❌ Нельзя удалить главного администратора!")
                else:
                    ADMIN_LIST.remove(new_admin)
                    save_admins(ADMIN_LIST)
                    await update.message.reply_text(f"✅ @{new_admin} удален из списка админов!")
            else:
                await update.message.reply_text(f"❌ @{new_admin} не найден в списке админов!")
        
        user_data.pop('admin_action', None)
        await admin_management(update, context)
        return
    
    # Редактирование позиции
    if 'editing' in user_data:
        editing = user_data['editing']
        category = editing['category']
        item = editing['item']
        
        # Обновляем цену
        PRICES[category][item] = message_text
        save_data(PRICES)
        
        await update.message.reply_text(
            f"✅ Цена обновлена!\n"
            f"📝 {item}: {message_text}"
        )
        
        user_data.clear()
        await edit_category(update, context, category)
        return
    
    # Добавление новой позиции
    if 'adding' in user_data:
        adding = user_data['adding']
        
        if adding['step'] == 'name':
            # Сохраняем название и запрашиваем цену
            user_data['adding']['name'] = message_text
            user_data['adding']['step'] = 'price'
            
            await update.message.reply_text(
                f"📝 <b>Название:</b> {message_text}\n\n"
                "Теперь отправьте цену для этой позиции.\n"
                "Пример: 50,000 - 70,000 ₽",
                parse_mode='HTML'
            )
            return
        
        elif adding['step'] == 'price':
            # Добавляем новую позицию
            category = adding['category']
            name = adding['name']
            price = message_text
            
            PRICES[category][name] = price
            save_data(PRICES)
            
            await update.message.reply_text(
                f"✅ Позиция добавлена!\n"
                f"📦 {name}: {price}\n"
                f"📁 Категория: {category}"
            )
            
            user_data.clear()
            await edit_category(update, context, category)
            return

# ========== ОСНОВНОЙ ОБРАБОТЧИК КНОПОК ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех inline кнопок"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    username = user.username
    data = query.data
    
    # Проверка прав для админских действий
    admin_actions = ['admin_', 'edit_', 'add_', 'remove_']
    if any(data.startswith(action) for action in admin_actions):
        if not username or not is_admin(username):
            await query.edit_message_text("❌ У вас нет доступа к админ-панели!")
            return
    
    # Основное меню
    if data == 'main':
        await start(update, context)
        return
    
    # Админ-панель
    elif data == 'admin_panel':
        await show_admin_panel(update, context)
    
    elif data == 'admin_edit':
        await admin_edit_menu(update, context)
    
    elif data == 'admin_manage':
        await admin_management(update, context)
    
    elif data == 'admin_stats':
        await show_stats(update, context)
    
    # Редактирование категорий
    elif data == 'edit_accessories':
        await edit_category(update, context, 'accessories')
    elif data == 'edit_cars':
        await edit_category(update, context, 'cars')
    elif data == 'edit_skins':
        await edit_category(update, context, 'skins')
    elif data == 'edit_houses':
        await edit_category(update, context, 'houses')
    
    # Редактирование конкретных позиций
    elif data.startswith('edit_'):
        await edit_item(update, context)
    
    # Добавление позиций
    elif data == 'add_item_menu':
        await add_item_menu(update, context)
    
    elif data == 'add_accessories':
        await add_item_prompt(update, context, 'accessories')
    elif data == 'add_cars':
        await add_item_prompt(update, context, 'cars')
    elif data == 'add_skins':
        await add_item_prompt(update, context, 'skins')
    elif data == 'add_houses':
        await add_item_prompt(update, context, 'houses')
    
    elif data.startswith('add_to_'):
        category = data.replace('add_to_', '')
        await add_item_prompt(update, context, category)
    
    # Управление админами
    elif data == 'add_admin':
        await add_admin_prompt(update, context)
    
    elif data == 'remove_admin':
        await remove_admin_prompt(update, context)
    
    # Пользовательское меню
    elif data == 'property':
        keyboard = [
            [InlineKeyboardButton("🕶 Аксессуары", callback_data='accessories')],
            [InlineKeyboardButton("🚗 Автомобили", callback_data='cars')],
            [InlineKeyboardButton("🎨 Скины", callback_data='skins')],
            [InlineKeyboardButton("🏡 Дома", callback_data='houses')],
            [InlineKeyboardButton("⬅️ Назад", callback_data='main')]
        ]
        await query.edit_message_text(
            "🏠 <b>Имущество</b>\nВыберите категорию:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
    
    elif data in ['accessories', 'cars', 'skins', 'houses']:
        category_name = {
            'accessories': 'Аксессуары',
            'cars': 'Автомобили',
            'skins': 'Скины',
            'houses': 'Дома'
        }[data]
        
        text = f"📊 <b>{category_name}:</b>\n\n"
        for item, price in PRICES[data].items():
            text += f"• <b>{item}</b>: {price}\n"
        
        keyboard = [[InlineKeyboardButton("⬅️ Назад к имуществу", callback_data='property')]]
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            
