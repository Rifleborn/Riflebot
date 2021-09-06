#comment - ctrl + /
#========================================================================================================
#tasks
#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#3. повідомлення в конкретний канал
#4. як відправляти емодзі
#5. вивід в лог чат
#6. команду help
#7. очистка БД (тільки адміністратором по ролі) !!!
#=======NEW=========
#8. /help
#9. робити зсув message_id при видаленні/очистці БД
#запис до БД повідомлень користувачів
import discord

from config import settings
from discord.ext import commands
from discord.utils import find
import sqlite3
import os

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), help_command=None)

Commands = {"/clear_db"}
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
    #channel = bot.get_channel(settings['чат'])
    await channel.send(f'Ready to engage')

@bot.command()
@commands.has_permissions(administrator=True)
async def clear_db(ctx):
    cursor.execute('DELETE FROM users_messages WHERE message_id > 0')
    sqlite_connection.commit()
    await ctx.send("Database cleared")
    print("Database cleared\n")

#context - same channel in which command (help) was writed
@bot.command()
async def help(ctx):
    await ctx.send("Custom help command")

@bot.command()
async def show(ctx):
    await ctx.send("dfadsfafdaest")

@bot.command()
async def ss(ctx):
    emoji = discord.utils.get(bot.emojis, name=':police:')
    await ctx.send(str(emoji))
    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')
    await ctx.send('<:police:>')

# commands
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    # insert message to DB if it isnt bot's message and not "/clear_db" command
    if (message.content != "/clear_db") and (message.author != bot.user):
        cursor.execute('INSERT INTO users_messages(user_id, message_text, message_date) VALUES(?, ?, ?)', (str(message.author), str(message.content), str(message.created_at)))
        sqlite_connection.commit()
        # debug
        print(f'User ID: {message.author}\nMessage: {message.content}\nDate/Time | UTC/(GMT+3)-3 hours: {message.created_at}\n')

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



