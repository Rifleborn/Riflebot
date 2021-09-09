#==================VER 0.0.2===================
# ctrl + /
# Project on discord API #Author: Rifleborn
# Python (discord.py, XLSX, sqlite3), SQL, Markdown
# XLSX writer docs https://xlsxwriter.readthedocs.io/tutorial01.html
# XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX file format.

#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#3. повідомлення в конкретний канал
#12. голосовуха
#13. закриття бд
#15. exception with connection to discord
#16. send command
#17. exception with command like "error command not found"
#18. глянути візуально на все що вміє бот, щось додумати ще
# send & markdown
# java програмку візуальну для налаштування конфіг файлу
# людський експорт в XLSX !!!
# RSS (Arma 3)
# ban command & banlist
# команда для виключення бота
# ClientConnectorError(req.connection_key, exc) from exc
# aiohttp.client_exceptions.ClientConnectorError:
# find hosting for bot
# all permissions in code NOT IN INVITE
# парсинг строки в команді get_latest
# xlsx нормальне форматування файлу, бо це фігня якась
# якщо немає БД - команду на створення з усіма відповідними колонками

import discord

from config import settings
from discord.ext import commands
from discord.utils import find
import xlsxwriter
import sqlite3
import os

#command prefix (was chosen acording to other bots prefix on server)
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), help_command=None)
Commands = ["/clear_db", "/help", "/fascist", "/get_latest", "/get_messages"]

# connecting to database
try:
    sqlite_connection = sqlite3.connect('users.db')
    cursor = sqlite_connection.cursor()
    print("Database created and successfully connected to SQLite")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("Database version SQLite: ", record)
    #cursor.close()

except sqlite3.Error as error:
    print("Error with connection to sqlite", error)

# finally:
#     if (sqlite_connection):
#         sqlite_connection.close()
#         print("Connection with SQLite closed")

#========================================================================================
#event when bot is online
@bot.event
async def on_ready():
    try:
        print('We have logged in as {0.user}\n'.format(bot))
        #getting channel by id (using development mod in discord)
        #channel = bot.get_channel(settings['TEST_CHANNEL'])
        #await channel.send(f'Ready to engage')
    except:
        print("Error with logging")

#==========commands (consist of def(async), and sending some info, media etc.============
#==========admin commands===========

@bot.command()
@commands.has_permissions(administrator=True)
async def clear_db(ctx):
    # WHERE message_id > 0
    cursor.execute('DELETE FROM users_messages')
    # UPDATE SQLITE_SEQUENCE SET user_id = 1 WHERE NAME = 'users_messages';
    tableName = "users_messages";
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='" + tableName + "'");
    sqlite_connection.commit()
    await ctx.send("Database cleared")
    print("Database cleared\n")

@bot.command()
@commands.has_permissions(administrator=True)
async def get_latest(ctx):
    # REWRITE THIS
    user_id_text = str(ctx.message.author);

    cursor.execute('SELECT message_id, user_id, message_text, message_date, server_name FROM users_messages '
                   'WHERE ((message_id = (SELECT MAX(message_id) FROM users_messages)) and (user_id = "' + user_id_text + '"))')
    sqlite_connection.commit()
    result = cursor.fetchone();

    # getting user_id and separating it from list
    user_id_text = result[1]
    result_list = list(result)
    result_list.pop(1)

    # output
    print("Latest message of",user_id_text)
    print(*result_list, "\n", sep = " | ",)

#get xlsx file
@bot.command()
@commands.has_permissions(administrator=True)
async def get_messages(ctx):
    # ======xlsx test============
    # create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('export/test.xlsx')
    worksheet = workbook.add_worksheet()

    cursor.execute('SELECT * '
                   'FROM users_messages')
    messages = cursor.fetchall()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Names for columns
    worksheet.write(row, col, "message_id")
    worksheet.write(row, col + 1, "user_id")
    worksheet.write(row, col + 2, "message_text")
    worksheet.write(row, col + 3, "message_date")
    worksheet.write(row, col + 4, "server_name")
    row+=1

    # Iterate over the data and write it out row by row.
    for message_id, user_id, message_text, message_date, server_name in (messages):
        worksheet.write(row, col, message_id)
        worksheet.write(row, col + 1, user_id)
        worksheet.write(row, col + 2, message_text)
        worksheet.write(row, col + 3, message_date)
        worksheet.write(row, col + 4, server_name)
        row += 1

    # Write a total using a formula.
    # worksheet.write(row, 0, 'Total')
    # worksheet.write(row, 1, '=SUM(B1:B4)')
    workbook.close()

    await ctx.send(file=discord.File(r'export/test.xlsx'))
    print("XSLX file sended.\n")

#=====================commands for all users==============================

#context or ctx - channel in which command (help) was writed

#custom help command
@bot.command()
async def help(ctx):
    #printing command list with sep
    commands_list = " "
    await ctx.send("```Custom help command```")
    await ctx.send(commands_list.join(Commands))

#test emoji command
@bot.command()
async def ss(ctx):
    emoji = discord.utils.get(bot.emojis, name=':police:')
    await ctx.send(str(emoji))
    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')
    await ctx.send('<:police:>')

#test command to get Guild(Server) name
@bot.command()
async def server(ctx):
    await ctx.send(ctx.guild.name)

# another type of commands (can't remember why i need it)
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    # insert message to DB if it isnt bot's message and not command
    if (message.content not in Commands) and (message.author != bot.user):
        cursor.execute('INSERT INTO users_messages(user_id, message_text, message_date, server_name) VALUES(?, ?, ?, ?)',
                       (str(message.author), str(message.content), str(message.created_at), str(message.guild.name)))
        sqlite_connection.commit()
        # debug
        print(f'User ID: {message.author}\nMessage: {message.content}\n'
              f'Date/Time | UTC/(GMT+3)-3 hours: {message.created_at}\n'
              f'Server: {message.guild.name}\n')

    # start for checking player commands
    if message.content.startswith('/'):
        if message.content.startswith('/hi'):
            # message with mention of author(user)
            await message.channel.send(f'Hello {message.author.mention}!')

        if message.content.startswith('/fascist'):
            # message with mention of author(user)
            await message.channel.send(f'{message.author.mention}')
            await message.channel.send(file=discord.File('images/bonov_eating.gif'))

        if message.content.startswith('/emoji'):
            await message.channel.send("<:police:884470225452560445>")
            #await message.channel.send(str(bot.get_emoji('884474673151221772')))
            #await message.channel.send("<:up10:12345>")


#launch
bot.run(settings['TOKEN'])

#async def emoji_url(ctx):
#    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')



