#==================VER 0.0.4===================
# Project on discord API #Author: Rifleborn
# Python (discord.py, XLSX, sqlite3, feedparser), SQL, Markdown
# XLSX writer docs https://xlsxwriter.readthedocs.io/tutorial01.html
# XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX file format.

#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#3. exception with connection to discord
#4. exception with command like "error command not found"
#5. глянути візуально на все що вміє бот, щось додумати ще

# java програмку візуальну для налаштування конфіг файлу
# ClientConnectorError(req.connection_key, exc) from exc
# aiohttp.client_exceptions.ClientConnectorError:
# find hosting for bot
# all permissions in code, NOT BY INVITE

# виключення
# ctx and username combination: async def kick(ctx, userName: discord.User)
# Кастомну роль боту в методі on_guild_join
# написати гру з ботом користувачем: бот створює чат для гри, користувачі мають команди які працюють тільки в цьому чаті,
# Ignoring exception in command None:
# discord.ext.commands.errors.CommandNotFound: Command "shudown" is not found

#====working on====
# RSS
# get_ban_data 'nick' NEED TEST
# ban 'nick' 'reason' NEED TEST
# ГОЛОСОВІ ПОВІДОМЛЕННЯ
# якщо немає БД - команду на створення з усіма відповідними колонками
# cursor.close()

# The venv module provides support for creating lightweight “virtual environments”
# with their own site directories, optionally isolated from system site directories.
# Each virtual environment has its own Python binary
# (which matches the version of the binary that was used to create this environment) and
# can have its own independent set of installed Python packages in its site directories

from config import settings
from discord.ext import commands

import discord
import feedparser
import xlsxwriter
import sqlite3
import os

#command prefix (was chosen acording to other bots prefix on server)
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), help_command=None)
#not all list of commands (command /help show all actual commands)
Commands = ["/help", "/clear_db table_name", "/get_message_date", "/fascist", "/get_latest", "/get_messages discord_tag", "/get_all"]

# RSS
post = feedparser.parse('https://arma3.com/rss')

print(post.feed.title)
print(post.feed.link)
print(post.feed.description)
print(post.feed.published)
print(post.feed.published_parsed)

# connecting to database
try:
    sqlite_connection = sqlite3.connect('users.db')
    cursor = sqlite_connection.cursor()
    print("Database created and successfully connected to SQLite")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("Database version SQLite: ", record)

    # re-creating
    # # rewrite
    # print("--Trying to create DB--")
    # sqlite_connection.execute('CREATE TABLE "users_messages" ('
    #                           '"message_id"	INTEGER NOT NULL UNIQUE,'
    #                           '"user_id"	TEXT,'
    #                           '"message_text"	TEXT,'
    #                           '"message_date"	TEXT,'
    #                           '"server_name"	TEXT,'
    #                           'PRIMARY KEY("message_id" AUTOINCREMENT));')
    # print("Database created and successfully connected to SQLite")
    #
    # sqlite_select_query = "select sqlite_version();"
    # cursor.execute(sqlite_select_query)
    # record = cursor.fetchall()
    # print("Database version SQLite: ", record)

except sqlite3.Error as error:
    print("---Error with connection to sqlite---", error)
    print(error)

#see why not async
async def export_xlsx(list_of_messages, file_name, ctx):
    #workbook(see on XLSX doc's)
    # create a workbook and add a worksheet (XLSX).
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

#def with clearing database tables
async def clear_db_def(table_name, ctx):
    cursor.execute('DELETE FROM "' + table_name + '"')
    # UPDATE SQLITE_SEQUENCE SET user_id = 1 WHERE NAME = 'users_messages';
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='" + table_name + "'");
    sqlite_connection.commit()
    await ctx.send("Table", table_name, "cleared")
    print("Database cleared\n")

#event when bot joined guild
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! this is the message i send when i join a server')
        break
int _you
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
# checking user's command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

#admin/owner commands
# command for banning users
@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason: str):
    if ctx.message.author.guild_permissions.administrator:
        await member.ban(reason = reason)

#The below code unbans player.
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    if ctx.message.author.guild_permissions.administrator:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

@bot.command()
async def shutdown(ctx):
    # @commands.is_owner()
    if ctx.message.author.guild_permissions.administrator:
        try:
            if (sqlite_connection):
                sqlite_connection.close()
                cursor.close()
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
async def clear_db(ctx, table_name: str):
    # equialent of @commands.has_permissions(administrator=True)
    if ctx.message.author.guild_permissions.administrator:
        if table_name == "banned_users" or table_name == "users_messages":
            clear_db_def(table_name, ctx)
        elif table_name == "all":
            clear_db_def("banned_users", ctx)
            clear_db_def("users_messages", ctx)
        else:
            await ctx.send("Wrong table name")
    else:
        print("---User have no permissions---")

#get_latest user message
@bot.command()
async def get_latest(ctx, user_tag: str):
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
    if ctx.message.author.guild_permissions.administrator:

        # REWRITE THIS
        cursor.execute('SELECT message_id, user_id, message_text, message_date, server_name FROM users_messages '
                   'WHERE user_id = "' + str(user_tag) + '"')
        sqlite_connection.commit()
        user_messages = cursor.fetchall();

        #getting xlsx file
        await export_xlsx(user_messages,user_tag,ctx)

        # getting user_id and separating it from list
        print("--All messages by", user_tag, "sended in XLSX file--\n")
    else:
        print("--User have no permissions--\n")

#get all user messages by data
@bot.command()
async def get_message_date(ctx, user_tag: str, messageDate: str):
    # equialent of @commands.has_permissions(administrator=True)
    if ctx.message.author.guild_permissions.administrator:
        print("DATE TEST: ", messageDate)
        print("user tag test: ", user_tag)
        # getting all messages by user tag and date
        try:
            cursor.execute('SELECT message_id, user_id, message_text, message_date, server_name FROM users_messages '
                           'WHERE ((message_date like "'+messageDate+'") and (user_id = "' + str(user_tag) + '"))')
                           #'WHERE ((CHARINDEX('+messageDate+', message_date) > 10)and (user_id = "' + str(user_tag) + '"))')
            sqlite_connection.commit()
            user_messages = cursor.fetchall();
        except Exception:
            print("CNAT LOAD THIS SHIT")
        #getting xlsx file
        file_name = user_tag + " " + messageDate
        await export_xlsx(user_messages,file_name,ctx)

        print("--All messages by ",user_tag, "|", messageDate, "sended in XLSX file--\n")
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
    await ctx.send("```Available commands```")
    helptext = "```"
    for command in bot.commands:
        helptext+=f'/{command}\n'
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
        messageDate = str(message.created_at);
        slice_object = slice(16)
        messageDate = messageDate[slice_object]

        try:
            cursor.execute('INSERT INTO users_messages(user_id, message_text, message_date, server_name) VALUES(?, ?, ?, ?)',
                           (str(message.author), str(message.content), messageDate, str(message.guild.name)))
            sqlite_connection.commit()
            # debug
            print(f'User ID(tag): {message.author}\nMessage: {message.content}\n'
                  f'Date/Time | UTC/(GMT+3)-3 hours: {message.created_at}\n'
                  f'Server: {message.guild.name}\n')
        except sqlite3.Error:
            print("---Command/message was not writted---")

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



