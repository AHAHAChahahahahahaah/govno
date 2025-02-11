import logging
from datetime import datetime, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from zoneinfo import ZoneInfo  # Используем zoneinfo вместо pytz

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = '7346330023:AAEeVut4TrKwZoYrqvsE_HLLKoDP0VKK1aI'

# Глобальный список chat_id, куда бот будет отправлять сообщения
active_chats = set()

# Функция для расчета дней до Нового года
def days_until_new_year():
    now = datetime.now(ZoneInfo('Asia/Yekaterinburg'))  # Используем ZoneInfo
    new_year = datetime(now.year + 1, 1, 1, tzinfo=ZoneInfo('Asia/Yekaterinburg'))
    if now > new_year:
        new_year = datetime(now.year + 1, 1, 1, tzinfo=ZoneInfo('Asia/Yekaterinburg'))
    return (new_year - now).days

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    active_chats.add(chat_id)  # Добавляем chat_id в список активных чатов
    await update.message.reply_text('Привет! Я буду сообщать количество дней до Нового года каждый день в 00:00 по Екатеринбургу. Также вы можете использовать команду /day, чтобы узнать количество дней до Нового года в любое время.')

# Команда /day
async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    days = days_until_new_year()
    await update.message.reply_text(f'До Нового года осталось {days} дней!')

# Функция для отправки сообщения
async def send_days_remaining(context: ContextTypes.DEFAULT_TYPE):
    days = days_until_new_year()
    for chat_id in active_chats:  # Отправляем сообщение во все активные чаты
        try:
            await context.bot.send_message(chat_id=chat_id, text=f'До Нового года осталось {days} дней!')
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик команды /day
    application.add_handler(CommandHandler("day", day))

    # Планирование ежедневного сообщения
    job_queue = application.job_queue
    job_queue.run_daily(send_days_remaining, time=time(0, 0, 0, tzinfo=ZoneInfo('Asia/Yekaterinburg')))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
