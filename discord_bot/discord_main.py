#==================VER 0.0.5===================
# Project on discord API #Author: Rifleborn
# Python (discord.py, XLSX, sqlite3, feedparser, request, BeatifulSoup), SQL, Markdown
# BeautifulSoup - навігація по структурі отриманого HTML файлу
# Request
# XLSX - створення книги з потрібними даними для виводу
# sqlite3 - БД
# feedparser - парсинг
# discord.py - API
# soupsieve - CSS selectors
# XLSX writer docs https://xlsxwriter.readthedocs.io/tutorial01.html
# XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX file format.

from config import settings
from discord.ext import commands,tasks

import discord
import feedparser
import xlsxwriter
import sqlite3
import traceback
import sys
from discord.ext.commands.errors import MemberNotFound
from discord.ext.commands import has_permissions
import uuid
import requests
import os
#from parsing import parse

#command prefix (was chosen acording to other bots prefix on server)
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all(), help_command=None)
#not all list of commands (command /help show all actual commands)
Commands = ["/help", "/clear_db table_name", "/get_message_date", "/get_messages discord_tag", "/get_all", "/shutdown"]
#pictures extensions
pic_ext = ['.jpg', '.png', '.jpeg']

# RSS
#getting url from config.py
post = feedparser.parse(settings['URL'])

# print(post.feed.title)
# print(post.feed.link)
# print(post.feed.description)
# print(post.feed.description)
# print(post.feed.published)
# print(post.feed.published_parsed)

# parse()

# connecting to database
try:
    sqlite_connection = sqlite3.connect('users.db')
    cursor = sqlite_connection.cursor()
    print("Database created and successfully connected to SQLite")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("Database version SQLite: ", record, "\n")

except sqlite3.Error as error:
    print("---Error with connection to sqlite---", error)
    sqlite_connection = sqlite3.connect('users.db')
    cursor = sqlite_connection.cursor()

    sqlite_connection.execute('CREATE TABLE "users_messages" ('
                              '"message_id"	INTEGER NOT NULL UNIQUE,'
                              '"user_id"	TEXT,'
                              '"message_text"	TEXT,'
                              '"message_date"	TEXT,'
                              '"server_name"	TEXT,'
                              '"attachment_name"	TEXT,'
                              'PRIMARY KEY("message_id" AUTOINCREMENT));')
    print("Database created and successfully connected to SQLite")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("Database version SQLite: ", record)

async def export_xlsx(list_of_messages, file_name, ctx):
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
    worksheet.set_column(0, 5, 24)

    # Names for columns
    worksheet.write(row, col, "message_id", column_name_cell)
    worksheet.write(row, col + 1, "user_id", column_name_cell)
    worksheet.write(row, col + 2, "message_text", column_name_cell)
    worksheet.write(row, col + 3, "message_date", column_name_cell)
    worksheet.write(row, col + 4, "server_name", column_name_cell)
    worksheet.write(row, col + 5, "attachment_name", column_name_cell)
    row += 1

    # Iterate over the data and write it out row by row.
    # if (list_of_messages.user_id != ""):
    for message_id, user_id, message_text, message_date, server_name, attachment_name in (list_of_messages):
        worksheet.write(row, col, message_id, data_cell)
        worksheet.write(row, col + 1, user_id, data_cell)
        worksheet.write(row, col + 2, message_text, data_cell)
        worksheet.write(row, col + 3, message_date, data_cell)
        worksheet.write(row, col + 4, server_name, data_cell)
        worksheet.write(row, col + 5, attachment_name, data_cell)
        row += 1
    workbook.close()
    await ctx.send(file=discord.File(r'export/' + file_name + '.xlsx'))

#def with clearing database tables
async def clear_db_def(table_name, ctx):
    cursor.execute('DELETE FROM "' + table_name + '"')
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='" + table_name + "'");
    sqlite_connection.commit()
    await ctx.send("Таблицю очищено.")
    print("--Database cleared--\n")

#event when bot joined guild
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Доєднався до сервера.')
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

#========================commands===========================
# @commands.Cog.listener()
# async def on_command_error(self, ctx, error):
#     if hasattr(ctx.command, 'on_error'):
#         return
# 
#     cog = ctx.cog
#     if cog:
#         if cog._get_overridden_method(cog.cog_command_error) is not None:
#             return
# 
#     ignored = (commands.CommandNotFound,)
#     error = getattr(error, 'original', error)
# 
#     if isinstance(error, ignored):
#         return
#     if isinstance(error, commands.DisabledCommand):
#         await ctx.send(f'{ctx.command} було виключено.')
#     elif isinstance(error, commands.BadArgument):
#         if ctx.command.qualified_name == 'tag list':
#             await ctx.send('Неможливо знайти цього користувача.')
#     #else:
#         # усі інші помилки
#         # print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
#         # traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

#admin/owner commands
@bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        if reason==None:
            reason = ''

        cursor.execute(
            'INSERT INTO banned_users(user_tag, ban_reason) '
            'VALUES(?, ?)', (str(member), reason))
        sqlite_connection.commit()
        await member.ban(reason=reason)
        await ctx.send(f'Користувача заблоковано.')
    except MemberNotFound as e:
        await ctx.send("Користувача не знайдено.")
        print("--Member not found--\n")


@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    try:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send('Користувача розбанено.')
                print('--Користувача розбанено--\n')
            else:
                await ctx.send('Користувач не заблокований на сервері.')
    except ValueError:
        await ctx.send('Введіть тег користувача - нік#0000')

@bot.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
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

@bot.command()
@commands.has_permissions(administrator=True)
async def clear_db(ctx, table_name: str):
        if table_name == "banned_users" or table_name == "users_messages":
            await clear_db_def(table_name, ctx)
        elif table_name == "all":
            await clear_db_def("banned_users", ctx)
            await clear_db_def("users_messages", ctx)
        else:
            await ctx.send("Wrong table name.")


#get all user messages
@bot.command()
async def get_messages(ctx, user_tag: str):
    # equialent of @commands.has_permissions(administrator=True)
    if ctx.message.author.guild_permissions.administrator:
        cursor.execute('SELECT message_id, user_id, message_text, message_date, server_name, attachment_name FROM users_messages '
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
@commands.has_permissions(administrator=True)
async def get_message_date(ctx, user_tag: str, messageDate: str):
        # getting all messages by user tag and date
        try:
            print("--user_tag--", user_tag)
            print("--messageDate--", messageDate)
            cursor.execute('SELECT message_id, user_id, message_text, message_date, server_name, attachment_name FROM users_messages '
                         #  'WHERE ((message_date like "'+messageDate+'") and (user_id = "' + str(user_tag) + '"))')
                           'WHERE ((instr(message_date, "'+str(messageDate)+'") > 0) and (user_id = "' + str(user_tag) + '"))')
#                           'WHERE user_id = "' + str(user_tag) + '"')
            sqlite_connection.commit()
            user_messages = cursor.fetchall();
        except Exception:
            print("--Can't load messages by date--\n")
        #getting xlsx file
        file_name = user_tag + " " + messageDate
        await export_xlsx(user_messages,file_name,ctx)

        print("--All messages by ",user_tag, "|", messageDate, "sended in XLSX file--\n")

#get xlsx file with all data from DB
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
#context or ctx - channel in which command was writed

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

#test command to get Guild(Server) name
@bot.command()
async def server(ctx):
    await ctx.send(ctx.guild.name)

# on message event (basic event)
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    messageText = message.content

    # processing if it isnt bot's message and not command
    if (message.author != bot.user):
        messageDate = str(message.created_at);
        slice_object = slice(16)
        messageDate = messageDate[slice_object]

        # if message have attachment
        attachmentName = ''
        try:
            url = message.attachments[0].url
        except IndexError:
            print("--Message attachment not found--")
        else:
            if url[0:26] == "https://cdn.discordapp.com":
               for attach in message.attachments:
                    attachmentName = attach.filename
                    await attach.save(f"attachments/{attach.filename}")
                    print('Message attachment: ' + attach.filename)

        try:
            cursor.execute('INSERT INTO users_messages(user_id, message_text, message_date, server_name, attachment_name) VALUES(?, ?, ?, ?, ?)',
                               (str(message.author), str(message.content), messageDate, str(message.guild.name), attachmentName))
            sqlite_connection.commit()

            print(f'User ID(tag): {message.author}\nMessage: {messageText}\n'
            f'Date/Time | UTC/(GMT+3)-3 hours: {message.created_at}\n'
            f'Server: {message.guild.name}\n')
        except sqlite3.Error:
            print("---Command/message was not writted---")

    # start for checking player commands
    if message.content.startswith('/'):
        if message.content.startswith('/hi'):
            # message with mention of author(user)
            await message.channel.send(f'Hello {message.author.mention}!')
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



