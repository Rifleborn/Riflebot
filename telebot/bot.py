#   python bot.py
import telebot
import config
import random
import os

import feedparser
import datetime
import configparser
import urllib.request, urllib.parse, urllib.error

from telebot import types

CONST_IMAGES_DIR = 'images';

bot = telebot.TeleBot(config.TOKEN)

config = configparser.ConfigParser()
config.read('settings.ini')
FEED = config.get('RSS', 'feed')
DATETIME = config.get('RSS', 'DATETIME')
rss = feedparser.parse(FEED)


@bot.message_handler(commands=['start'])

def welcome(message):


    for post in reversed(rss.entries):
        data = post.published
        time = datetime.datetime.strptime(data, '%a, %d %b %Y %H:%M:%S %z')
        time_old = config.get('RSS', 'DATETIME')
        time_old = datetime.datetime.strptime(time_old, '%Y-%m-%d  %H:%M:%S%z')

        print(time)
        print(time_old)

        if time <= time_old:
            continue
        else:
            config.set('RSS', 'DATETIME', str(time))
            with open('settings.ini', "w") as config_file:
                config.write(config_file)

        print('---------------------------------')
        print(time)

        text = post.title
        print(text)

        img = post.links[1].href
        print(img)

        link = post.links[0].href
        print(link)

        urllib.request.urlretrieve(img, 'img.jpg')

        bot.send_photo(message.chat.id, open('img.jpg', 'rb'))
        bot.send_message(message.chat.id, '<a href="' + link + '">' + text + '</a>', parse_mode='HTML')

    user_markup = telebot.types.ReplyKeyboardMarkup(True);
    user_markup.row('/start', '/stop');
    user_markup.row('RSS', '2');

 
@bot.message_handler(content_types=['text'])
def msg_handler(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Число (будь-яке)':
            bot.send_message(message.chat.id, str(random.randint(0,30)))

        elif message.text == 'Як справи?':
 
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Добре", callback_data='good')
            item2 = types.InlineKeyboardButton("Не дуже", callback_data='bad')
 
            markup.add(item1, item2)
 
            bot.send_message(message.chat.id, 'Чудово, як сам?', reply_markup=markup)

        elif message.text == 'Канали':
            markup = types.InlineKeyboardMarkup()
            bot.send_message(message.chat.id, 'Ось посилання:', parse_mode='html', reply_markup=markup)
   

        elif message.text == '/stop':
            bot.send_message(message.chat.id, 'Бувай.')
            bot.stop_polling()

        else:
            bot.send_message(message.chat.id, 'Не маю що відповісти')

 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass()


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Бувай.", reply_markup = hide_markup)
    bot.stop_polling()
# RUN
bot.polling(none_stop=True)