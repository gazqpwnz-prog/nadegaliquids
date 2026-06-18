
import asyncio
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ======== КОНФИГУРАЦИЯ ========
BOT_TOKEN = "8906080480:AAFQB5dZcbVlubxT9pPxLxz5XmlF1kP4jT0"  # ЗАМЕНИТЕ НА СВОЙ ТОКЕН!
WEB_APP_URL = "https://your-domain.com"  # ЗАМЕНИТЕ НА URL ВАШЕГО САЙТА!
ADMIN_IDS = [6602618961]  # Добавьте сюда ID администраторов

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======== КОМАНДЫ ========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    user = update.effective_user

    keyboard = [
        [InlineKeyboardButton("🛍️ Каталог", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("📦 Мои заказы", callback_data="orders")],
        [InlineKeyboardButton("💬 Поддержка", url="https://t.me/your_support")]
    ]

    welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в <b>MARKET USS</b>!

🛒 Здесь вы найдёте:
• Жидкости для вейпов
• POD-системы и устройства
• Расходники и аксессуары

Нажмите кнопку ниже, чтобы открыть каталог 👇
    """

    await update.message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    await update.message.reply_text("""
📋 <b>Команды бота:</b>

/start — Открыть главное меню
/catalog — Открыть каталог товаров
/cart — Посмотреть корзину
/support — Связаться с поддержкой

💡 Просто нажмите кнопку <b>«Каталог»</b>, чтобы начать покупки!
    """, parse_mode="HTML")

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Открыть каталог"""
    keyboard = [[InlineKeyboardButton("🛍️ Открыть каталог", web_app=WebAppInfo(url=WEB_APP_URL))]]
    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы открыть каталог товаров:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка данных из Web App"""
    data = json.loads(update.effective_message.web_app_data.data)

    if data.get("action") == "order":
        items = data.get("items", [])
        total = data.get("total", 0)
        user = update.effective_user

        # Формируем сообщение о заказе
        order_text = f"""
🛒 <b>Новый заказ!</b>

👤 Покупатель: @{user.username or 'нет'} (ID: {user.id})
📋 Товары:
"""
        for item in items:
            order_text += f"• {item['name']} x{item['qty']} — {item['price'] * item['qty']} ₽\n"

        order_text += f"\n💰 <b>Итого: {total} ₽</b>"

        # Отправляем админам
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(admin_id, order_text, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Не удалось отправить заказ админу {admin_id}: {e}")

        # Подтверждение пользователю
        await update.message.reply_text(
            f"✅ Заказ принят!\n\nСумма: <b>{total} ₽</b>\n\nМы свяжемся с вами для подтверждения.",
            parse_mode="HTML"
        )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ-панель"""
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ У вас нет доступа к админ-панели.")
        return

    keyboard = [
        [InlineKeyboardButton("➕ Добавить товар", web_app=WebAppInfo(url=f"{WEB_APP_URL}?admin=1"))],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("📦 Заказы", callback_data="orders_admin")]
    ]

    await update.message.reply_text(
        "🛠️ <b>Админ-панель</b>\n\nВыберите действие:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ======== ОБРАБОТКА ОШИБОК ========
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")

# ======== ЗАПУСК ========
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("catalog", catalog))
    application.add_handler(CommandHandler("admin", admin_panel))

    # Обработка данных из Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Обработка ошибок
    application.add_error_handler(error_handler)

    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
