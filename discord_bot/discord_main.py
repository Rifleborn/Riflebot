#==================VER 0.0.3===================
# Project on discord API #Author: Rifleborn
# Python (discord.py, XLSX, sqlite3), SQL, Markdown
# XLSX writer docs https://xlsxwriter.readthedocs.io/tutorial01.html
# XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX file format.

#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#12. голосовуха
#15. exception with connection to discord
#17. exception with command like "error command not found"
#18. глянути візуально на все що вміє бот, щось додумати ще

# java програмку візуальну для налаштування конфіг файлу
# RSS (Arma 3)
# ban command & banlist
# ClientConnectorError(req.connection_key, exc) from exc
# aiohttp.client_exceptions.ClientConnectorError:
# find hosting for bot
# all permissions in code NOT IN INVITE
# парсинг строки в команді get_latest
# якщо немає БД - команду на створення з усіма відповідними колонками
# get_message нік/дата
# пропрацювати над виключеннями
# - в день 1-3 завдання
# ctx and username combination: async def kick(ctx, userName: discord.User):
# Кастомну роль боту в методі on_guild_join
# написати гру з ботом користувачем: бот створює чат для гри, користувачі мають команди які працюють тільки в цьому чаті,
# ГОЛОСОВІ ПОВІДОМЛЕННЯ
# Ignoring exception in command None:
# discord.ext.commands.errors.CommandNotFound: Command "shudown" is not found
# вивід всіх повідомлень користувача через get_messages 'nick'
# get_ban_data 'nick'
# ban 'nick' 'reason'
# get_all_messages

import discord

from config import settings
from discord.ext import commands
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

#see why not async
async def export_xlsx(list_of_messages, file_name, ctx):
    #workbook(see on XLSX doc's)
    #================================XLSX=========================================
    # create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('export/' + file_name + '.xlsx')
    worksheet = workbook.add_worksheet()

    # style for cells
    data_cell = workbook.add_format({'border': 1, 'bg_color': '#E1E4E3'})
    column_name_cell = workbook.add_format({'border': 1, 'bg_color': '#79AD74'})

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Resize columns
    worksheet.set_column(0, 4, 24)

    # Names for columns
    worksheet.write(row, col, "message_id", column_name_cell)
    worksheet.write(row, col + 1, "user_id", column_name_cell)
    worksheet.write(row, col + 2, "message_text", column_name_cell)
    worksheet.write(row, col + 3, "message_date", column_name_cell)
    worksheet.write(row, col + 4, "server_name", column_name_cell)
    row += 1

    # Iterate over the data and write it out row by row.
    for message_id, user_id, message_text, message_date, server_name in (list_of_messages):
        worksheet.write(row, col, message_id, data_cell)
        worksheet.write(row, col + 1, user_id, data_cell)
        worksheet.write(row, col + 2, message_text, data_cell)
        worksheet.write(row, col + 3, message_date, data_cell)
        worksheet.write(row, col + 4, server_name, data_cell)
        row += 1

    workbook.close()
    await ctx.send(file=discord.File(r'export/' + file_name + '.xlsx'))

#event when bot joined guild
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! this is the message i send when i join a server')
        break

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

#========================commands (consist of def(async)=========================
#admin/owner commands
@bot.command()
async def shutdown(ctx):
    # @commands.is_owner()
    if ctx.message.author.guild_permissions.administrator:
        try:
            if (sqlite_connection):
                sqlite_connection.close()
                print("--Connection with SQLite closed--")

            try:
                await ctx.bot.logout()
                print("--Bot disabled--")
            except RuntimeError:
                print("--Event loop is closed")
        except sqlite3.Error:
            print("!-Shutdown error-!")
    else:
        print("---User have no permissions---")

@bot.command()
async def ban(ctx):
    #    async def kick(ctx, userName: discord.User):
    if ctx.message.author.guild_permissions.administrator:
        print("banned test")
    else:
        print("--User have no permissions for ban--")

@bot.command()
async def clear_db(ctx, table_name: str):
    # equialent of @commands.has_permissions(administrator=True)
    if ctx.message.author.guild_permissions.administrator:
        if table_name == "banned_users" or table_name == "users_messages":
            clear_db_def(table_name)
        elif table_name == "all":
            clear_db_def("banned_users")
            clear_db_def("users_messages")
        else:
            await ctx.send("Wrong table name")
    else:
        print("---User have no permissions---")

    async def clear_db_def(table_name):
        cursor.execute('DELETE FROM "'+table_name+'"')
        # UPDATE SQLITE_SEQUENCE SET user_id = 1 WHERE NAME = 'users_messages';
        cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='" + table_name + "'");
        sqlite_connection.commit()
        await ctx.send("Table", table_name, "cleared")
        print("Database cleared\n")

#get_latest user message
@bot.command()
async def get_latest(ctx, user_tag: str):
    # ctx and username combination: async def kick(ctx, userName: discord.User):
    # equialent of @commands.has_permissions(administrator=True)
    if ctx.message.author.guild_permissions.administrator:

        cursor.execute('SELECT message_id, user_id, message_text, message_date, server_name FROM users_messages '
                   'WHERE ((message_id = (SELECT MAX(message_id) FROM users_messages)) and (user_id = "' + str(user_tag) + '"))')
        sqlite_connection.commit()
        result = cursor.fetchone();

        await ctx.send("Database cleared")
        # getting user_id and separating it from list
        user_id_text = result[1]
        result_list = list(result)
        result_list.pop(1)

        #output
        print("Latest message of ",user_id_text)
        print(*result_list, "\n", sep = " | ",)
    else:
        print("---User have no permissions---")

#get all user messages
@bot.command()
async def get_messages(ctx, user_tag: str):
    # equialent of @commands.has_permissions(administrator=True)
    print("/get_messages, user_tag:", user_tag)
    if ctx.message.author.guild_permissions.administrator:

        # REWRITE THIS
        cursor.execute('SELECT message_id, user_id, message_text, message_date, server_name FROM users_messages '
                   'WHERE user_id = "' + str(user_tag) + '"')
        sqlite_connection.commit()
        user_messages = cursor.fetchall();

        #getting xlsx file
        await export_xlsx(user_messages,user_tag,ctx)

        # getting user_id and separating it from list
        user_id_text = user_messages[1]
        result_list = list(user_messages)
        result_list.pop(1)
        print("--All messages by ",user_id_text, "sended in XLSX file--\n")
    else:
        print("--User have no permissions--\n")

#get xlsx file
@bot.command()
async def get_all(ctx):
    if ctx.message.author.guild_permissions.administrator:
        cursor.execute('SELECT * '
                       'FROM users_messages')
        sqlite_connection.commit()
        messages = cursor.fetchall()

        file_name = "all_messages"
        await export_xlsx(messages, file_name, ctx)
        print("--All messages sended--\n")
    else:
        print("---User have no permissions---\n")

#=====================commands for all users==============================
#context or ctx - channel in which command (help) was writed

#custom help command
@bot.command()
async def help(ctx):
    #printing command list
    await ctx.send("```Available commands '/'```")
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

#test emoji command
@bot.command()
async def test(ctx):
    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')


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
        try:
            cursor.execute('INSERT INTO users_messages(user_id, message_text, message_date, server_name) VALUES(?, ?, ?, ?)',
                           (str(message.author), str(message.content), str(message.created_at), str(message.guild.name)))
            sqlite_connection.commit()
            # debug
            print(f'User ID(tag): {message.author}\nMessage: {message.content}\n'
                  f'Date/Time | UTC/(GMT+3)-3 hours: {message.created_at}\n'
                  f'Server: {message.guild.name}\n')
        except sqlite3.Error:
            print("---command/message was not writted, DB was closed before---")

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
#launch
bot.run(settings['TOKEN'])

# NOT DELETE THIS
# auto - role
# @Client.event
# async def on_member_join(member):
#     role = discord.utils.get(member.guild.roles, name='Unverified')
#     await member.add_roles(role)



