import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Инициализация API ключей
openai.api_key = 'YOUR_OPENAI_API_KEY'
telegram_bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Добро пожаловать в Подземелья и драконы! Напишите "начать", чтобы начать ваше приключение.'
    )

# Функция для обработки текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Пример простого взаимодействия с ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Ты мастер игры в Подземелья и драконы. Игрок говорит: {user_message}",
        max_tokens=150
    )

    # Отправка ответа пользователю
    update.message.reply_text(response.choices[0].text)

# Настройка бота
def main() -> None:
    updater = Updater(token=telegram_bot_token)
    dispatcher = updater.dispatcher

    # Обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
