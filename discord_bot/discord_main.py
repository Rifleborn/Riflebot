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

#command prefix (was chosen acording to other bots prefix on server)
bot = commands.Bot(command_prefix='/')

client = discord.Client()

@client.event
async def on_ready(ctx):
   await ctx.send('Hello')

#commands (consist of def(async), and sending some info, media etc.
@bot.command()
async def фашист(ctx):
    # await ctx.send('https://cdn.discordapp.com/attachments/836508755188514816/882245118613127168/IMG_20191226_195441_-_.jpg')
    await ctx.send(file=discord.File('images/bonov_eating.gif'))

@bot.command()
async def what_to_play(ctx):
    await ctx.send('Arma 3')
    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')

#launch
bot.run(settings['TOKEN'])