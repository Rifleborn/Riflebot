#comment - ctrl + /
#========================================================================================================
#tasks
#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#3. повідомлення в конкретний канал
#4. як відправляти емодзі
#5. вивід в лог чат
#6. команду help
import discord

from config import settings
from discord.ext import commands
from discord.utils import find
import sqlite3
import os

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), help_command=None)

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
#         print("Соединение с SQLite закрыто")

#========================================================================================
#event when bot is online
@bot.event
async def on_ready():
    print('We have logged in as {0.user}\n'.format(bot))
    #getting channel by id (using development mod in discord)
    channel = bot.get_channel(settings['TEST_CHANNEL'])
    await channel.send(f'Ready to engage')

@bot.command()
async def help(context):
    await context.send("Custom help command")

@bot.event
async def on_message(message):
    # if this message author is our bot(client)
    if message.author == bot.user:
        return

    #insert data (using ? for safety inserting without SQL injections
    cursor.execute('INSERT INTO users_messages VALUES(?, ?, ?)', (str(message.author), str(message.content), 'ff'))

    sqlite_connection.commit()

    print(f'User ID: {message.author}\nMessage: {message.content}\n')
    # start for checking player commands
    if message.content.startswith('/'):
        if message.content.startswith('/hi'):
            # message with mention of author(user)
            await message.channel.send(f'Hello {message.author.mention}!')
        if message.content.startswith('/fascist'):
            # message with mention of author(user)
            await message.channel.send(f'{message.author.mention}')
            await message.channel.send(file=discord.File('images/bonov_eating.gif'))

#launch
bot.run(settings['TOKEN'])
#============================================OLD============================================================
# discord client object
#client = discord.Client()

#command prefix (was chosen acording to other bots prefix on server)
#client = commands.Bot(command_prefix='/') NOT WORKS PROPERLY
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#
# @client.event
# async def on_message(message):
#     # if this message author is our bot(client)
#     if message.author == client.user:
#         return
#     #prefix
#     print(f'User ID: {message.author}\nMessage: {message.content}\n')
#     if message.content.startswith('/'):
#         if message.content.startswith('/hi'):
#             # message with mention of author(user)
#             await message.channel.send(f'Hello {message.author.mention}!')
#         if message.content.startswith('/fascist'):
#             # message with mention of author(user)
#             await message.channel.send(f'{message.author.mention}')
#             await message.channel.send(file=discord.File('images/bonov_eating.gif'))

#commands (consist of def(async), and sending some info, media etc.

#@client.command()
#async def fascist(ctx):
    # await ctx.send('https://cdn.discordapp.com/attachments/836508755188514816/882245118613127168/IMG_20191226_195441_-_.jpg')
#    await ctx.send(file=discord.File('images/bonov_eating.gif'))

#@client.command()
#async def what_to_play(ctx):
#    await ctx.send('Arma 3')
#    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')



