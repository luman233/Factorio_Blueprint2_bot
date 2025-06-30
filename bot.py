import os
import json
from telegram import Bot, TelegramError, InlineKeyboardMarkup, InlineKeyboardButton

# Конфиг из переменных окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID'))
THREAD_ID = int(os.getenv('TELEGRAM_THREAD_ID'))

STATE_FILE = 'state.json'
bot = Bot(token=TOKEN)

# Текст сообщения и кнопки
message_text = (
    "<b>🔷 Что должно быть в посте:</b>\n"
    "<b>1. Название —</b> кратко отражает суть, например: «Набор чертежей для ситиблоков»\n"
    "<b>2. Описание —</b> что делает чертёж, какие задачи решает, можно указать эффективность (например, производство ресурсов в секунду).\n"
    "<b>3. Изображения —</b> от 1 до 5 скриншотов. Видео можно, но нежелательно.\n"
    "<b>4. Ссылка или файл —</b> <i>txt</i> чертежа для использования другими игроками.\n"
    "По желанию: <i>теги.</i>\n\n"
)

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📋 Инструкция", url="https://telegra.ph/CHertezhi-06-11"),
        InlineKeyboardButton("ℹ️ Подробнее", url="https://t.me/FCTostin/414/447")
    ]
])

# Загрузка состояния
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
else:
    state = {}

old_message_id = state.get('message_id')

try:
    # Удалить старое сообщение, если есть
    if old_message_id:
        try:
            bot.delete_message(chat_id=CHAT_ID, message_id=old_message_id)
            print(f"Удалено старое сообщение с ID: {old_message_id}")
        except TelegramError as e:
            print(f"Не удалось удалить предыдущее сообщение: {e}")

    # Отправить новое сообщение
    new_message = bot.send_message(
        chat_id=CHAT_ID,
        text=message_text,
        parse_mode='HTML',
        reply_markup=keyboard,
        disable_notification=True,
        message_thread_id=THREAD_ID
    )
    print(f"Новое сообщение отправлено с ID: {new_message.message_id}")

    # Сохранить новое состояние
    state['message_id'] = new_message.message_id
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

except TelegramError as e:
    print(f"Ошибка: {e}")
