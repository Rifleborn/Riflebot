# бот отсилає фото і всю фігню
# розбрітись що за markup

#tasks:
#1. Взяття тексту, відсилання його ботом(створити кнопку яка буде витягувти з ДС новину)
#2. Створити проміжне сховище всіх новин(хз як працюватиме)
#3. RSS розібратись що це (https://arma3.com/ і по можливості сервери ДС)



#   автор Rifleborn
#   cd c:\Users\User\Desktop\bot\
#   python bot.py
import telebot
import config
import random
import os

#rss shit idk what it is
import feedparser
import datetime
import configparser
import urllib.request, urllib.parse, urllib.error

from telebot import types

#=====================початок коду де купа всього з чим треба розбиратись=============================
CONST_IMAGES_DIR = 'images';
# схоже дістаємо унікальний токен з конфігу
bot = telebot.TeleBot(config.TOKEN)

# налаштування з файлу settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')
FEED = config.get('RSS', 'feed')
DATETIME = config.get('RSS', 'DATETIME')
rss = feedparser.parse(FEED)


# handler на команду старт
@bot.message_handler(commands=['start'])
# функція, по суті початок "програми"
def welcome(message):
    # ===============RSS shit======================

    for post in reversed(rss.entries):
        data = post.published
        time = datetime.datetime.strptime(data, '%a, %d %b %Y %H:%M:%S %z')
        time_old = config.get('RSS', 'DATETIME')
        time_old = datetime.datetime.strptime(time_old, '%Y-%m-%d  %H:%M:%S%z')

        print(time)
        print(time_old)
        # Пропускаем уже опубликованные посты
        if time <= time_old:
            continue
        else:
            # Записываем время и дату нового поста в файл
            config.set('RSS', 'DATETIME', str(time))
            with open('settings.ini', "w") as config_file:
                config.write(config_file)

        print('---------------------------------')
        print(time)

        # Получаем заголовок поста
        text = post.title
        print(text)

        # Получаем картинку
        img = post.links[1].href
        print(img)

        # Получаем ссылку на пост
        link = post.links[0].href
        print(link)

        # Скачиваем картинку
        urllib.request.urlretrieve(img, 'img.jpg')

        # Отправляем картинку и текстовое описание в Telegram
        bot.send_photo(message.chat.id, open('img.jpg', 'rb'))
        bot.send_message(message.chat.id, '<a href="' + link + '">' + text + '</a>', parse_mode='HTML')

    # ===============end of RSS====================

    #=============
    user_markup = telebot.types.ReplyKeyboardMarkup(True);
    user_markup.row('/start', '/stop');
    user_markup.row('RSS', '2');
    user_markup.row('3', 'закинути гроші спільноті(ЗРОБИТИ ОПЛАТУ ТУТ)', 'Discord-сервери');
    bot.send_message(message.from_user.id, 'Ласкаво просимо в цю нову сучасну Україну', reply_markup=user_markup);
 
@bot.message_handler(content_types=['text'])
def some_shit(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Число будь яке взагалі пофік':
            bot.send_message(message.chat.id, str(random.randint(0,30)))

        elif message.text == '😊 Як справи?':
 
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Добре", callback_data='good')
            item2 = types.InlineKeyboardButton("Не дуже", callback_data='bad')
 
            markup.add(item1, item2)
 
            bot.send_message(message.chat.id, 'Чудово, як сам?', reply_markup=markup)

        # посилання на discord спільноти
        elif message.text == 'Канали':
        # розбіратись що це значить
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Arma 3 Ukraine", url="https://discord.gg/DYA3dNS"))
            bot.send_message(message.chat.id, 'Ось посилання:', parse_mode='html', reply_markup=markup)
   
        elif message.text == 'Чорт' or message.text == 'чорт':

        #send_random_picture
            all_files_in_directory = os.listdir(CONST_IMAGES_DIR)
        #директорія з фоткою
            file = random.choice(all_files_in_directory)
            photo = open('images' + '/' + file, 'rb')
        #підпис до фото
            caption = "нижній текст"
        #відіслати фото
            bot.send_photo(message.chat.id, photo, caption)
            photo.close();

        elif message.text == 'RSS':
            bot.send_message(message.chat.id, 'Бувай.')
            bot.stop_polling();

        elif message.text == '/stop':
            bot.send_message(message.chat.id, 'Бувай.')
            bot.stop_polling();

        else:
            bot.send_message(message.chat.id, 'Поняття не маю що відповісти 😢')

 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'От і добре 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бува 😢')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Як справи?",
                reply_markup=None)
 
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text="!ТЕКСТОВЕ ПОВІДОМЛЕННЯ!")
 
    except Exception as e:
        print(repr(e))

# НЕ РОБИТЬ, ЗРОБИВ ЧЕРЕЗ КОСТИЛЬ ВИЩЕ
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Бувай.", reply_markup = hide_markup)
    bot.stop_polling()
# RUN
bot.polling(none_stop=True)