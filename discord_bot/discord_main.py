#comment - ctrl +
# Rifleborn bot project on discord API
# markdown, python, SQL

#==================================VER 0.0.2======================================================================
#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#3. повідомлення в конкретний канал
#6. /команду help DONE
#7. очистка БД (тільки адміністратором по ролі) !!! DONE
#9. робити зсув message_id при видаленні/очистці БД
#10. /get_latest - найостанніше повідомлення від користувача NEED FIX BY USER_NAME
#11. читання rss з сайта і відсилання в діскорд
#12. голосовуха
#13. закриття бд
#14. колонку в БД з назвою сервера звідки прийшло повідомлення
#15. exception with connection to discord
#16. send command
#17. exception with command like "error command not found"

# ClientConnectorError(req.connection_key, exc) from exc
# aiohttp.client_exceptions.ClientConnectorError:

import discord

from config import settings
from discord.ext import commands
from discord.utils import find
import sqlite3
import os

#command prefix (was chosen acording to other bots prefix on server)
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), help_command=None)
Commands = ["/clear_db", "/help", "/fascist", "/get_latest_message"]

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
        channel = bot.get_channel(settings['TEST_CHANNEL'])
        #channel = bot.get_channel(settings['чат'])
        await channel.send(f'Ready to engage')
    except:
        print("Error with logging")

#==========commands (consist of def(async), and sending some info, media etc.============

#==========admin commands===========
#clearing DB
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

#getting latest user's message
@bot.command()
@commands.has_permissions(administrator=True)
async def get_latest(ctx):
    user_id_text = ctx.message.author.name;
    cursor.execute('SELECT user_id, message_text, message_date '
                   'FROM users_messages '
                   'WHERE ((message_id = (SELECT MAX(message_id) FROM users_messages)) and (user_id = "{user_id_text}"))')
    #print("===Last message of user ", user_id_text)
    for row in cursor:
        print(row)
    sqlite_connection.commit()

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

    # insert message to DB if it isnt bot's message and not "/clear_db" command
    if (message.content != "/clear_db") and (message.author != bot.user):
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
#============================================OLD============================================================
#@client.command()
#async def what_to_play(ctx):
#    await ctx.send('Arma 3')
#    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')



