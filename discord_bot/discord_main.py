#comment - ctrl + /
#=================
#tasks
#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#3. повідомлення в конкретний канал
#4. як відправляти емодзі
import discord

#setting import
from config import settings
from discord.ext import commands
from discord.utils import find

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}\n'.format(bot))

@bot.event
async def on_message(message):
    # if this message author is our bot(client)
    if message.author == bot.user:
        return

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



