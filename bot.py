import openai
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask, request
import threading

# Инициализация API ключей
openai.api_key = 'YOUR_OPENAI_API_KEY'
telegram_bot_token = '7299461708:AAGYktGsdHecI19BfHVK5F_KBw8rDso674g'

# Хранилище для команд
teams = {}
team_size = 5

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Добро пожаловать в Подземелья и драконы! Напишите /join для присоединения к команде.'
    )

# Функция для присоединения к команде
def join(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username or update.message.from_user.first_name
    team_id = None

    for tid, members in teams.items():
        if len(members) < team_size:
            team_id = tid
            break

    if team_id is None:
        team_id = len(teams) + 1
        teams[team_id] = []

    teams[team_id].append(user_id)

    if len(teams[team_id]) == team_size:
        update.message.reply_text(f'Команда {team_id} готова к игре! Участники: {", ".join(str(m) for m in teams[team_id])}')
    else:
        update.message.reply_text(f'Вы присоединились к команде {team_id}. Ожидаем еще {team_size - len(teams[team_id])} участников.')

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
    dispatcher.add_handler(CommandHandler('join', join))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота в отдельном потоке
    updater.start_polling()

# Flask сервер для поддержки активности на Glitch
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=main).start()
    app.run(host='0.0.0.0', port=3000)

