#tasks
#1. додати автовидачу ролі боту при доєднанні на сервер
#2. зробити відправку повідомлення по таймінгу 14сек 88 мілісекунд (типу того)
#3. повідомлення в конкретний канал
#4. як відправляти емодзі
import discord
from discord.ext import commands
from discord.utils import find

#префікс для команд (обраний відповідно до вже зайнятих префіксів ботів які є на сервері)
bot = commands.Bot(command_prefix='/')

client = discord.Client()

@client.event
async def on_ready(ctx):
   await ctx.send('Слава Україні!')

# ctx = channel
@bot.command()
async def привітання(ctx):
    await ctx.send('Ярослав Чижмар привіт!')
    await ctx.send(:a3coop_nice:)

@bot.command()
async def вигук(ctx):
    await ctx.send('Слава Україні! Героям Слава! Путін хуйло!')

@bot.command()
async def Стерненко(ctx):
    await ctx.send('фашист')

@bot.command()
async def СС(ctx):
    await ctx.send('Сергей Стерненко')

@bot.command()
async def бог(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/836508755188514816/882243891410116669/Yadsadrik.png')

@bot.command()
async def розшук(ctx):
    await(ctx.send('УВАГА!УВАГА! Позивний "Дєд", лідер укр розвідки, розшукується ВСП за те шо вкрав трактори'))
    await ctx.send('https://cdn.discordapp.com/attachments/836508755188514816/882244443791560744/grandpa.png')

@bot.command()
async def дитина_нації(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/836508755188514816/882244634380755014/IMG_20190824_161526.jpg')

@bot.command()
async def президент(ctx):
    #await ctx.send('https://cdn.discordapp.com/attachments/836508755188514816/882245118613127168/IMG_20191226_195441_-_.jpg')
    await ctx.send(file=discord.File('images/grandpa.png'))

@bot.command()
async def фашист(ctx):
    # await ctx.send('https://cdn.discordapp.com/attachments/836508755188514816/882245118613127168/IMG_20191226_195441_-_.jpg')
    await ctx.send(file=discord.File('images/bonov_eating.gif'))

@bot.command()
async def найкраща_гра(ctx):
    await ctx.send('Глобал мобілізейшн')
    await ctx.send('https://cdn.discordapp.com/emojis/784455362140569610.png?size=64')

bot.run('NzUzMjc2MzU4MjU1NDQzOTg5.X1j1Rw.dKNqUMS7vk4KAMw3Bken7OlZHqQ')