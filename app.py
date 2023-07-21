from flask import Flask, request
import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv('.env')
app = Flask(__name__)

TOKEN = os.environ.get('TOKEN', '')
bot = telebot.TeleBot(TOKEN)

programs = {}
with open('data.txt', encoding='utf-8') as file:
    for line in file:
        item, link = line.split(';')
        programs[item.strip()] = link.strip()


@bot.message_handler(commands=['start'])
def handler_start(message):
    bot.send_message(chat_id=message.chat.id, text='Hello')


@bot.message_handler(commands=['programs'])
def handler_programs(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for item, link in programs.items():
        button = types.InlineKeyboardButton(text=item, url=link)
        keyboard.add(button)
    bot.send_message(chat_id=message.chat.id, text='Оберіть програму навчання', reply_markup=keyboard)


@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'Test Bot', 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://gleeful-malasada-c187d5.netlify.app' + TOKEN)
    return 'Test Bot', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    bot.polling()