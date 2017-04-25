import discord, asyncio, random, re
from discord.ext import commands

client = discord.Client()

#bot = commands.Bot(command_prefix='!', description='This bot responds to commands with a quote... for now')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        with open('quotes.txt', 'r') as quoted_text:
            for line in quoted_text:
                if line.startswith(message.content):
                    msg = line
                    await client.send_message(message.channel, line.replace(str(message.content), ''))

# @bot.event
# async def on_ready():
#     print('Logged in as')
#     print(bot.user.name)
#     print(bot.user.id)
#     print('----')
#
# @bot.group(pass_context=True)
# async def quote(qt):
#     if qt.invoked_subcommand is None:
#         await bot.say('You forgot to tell me which quote you want')
#
# @quote.command()
# async def split():
#     with open('quotes.txt', 'r') as quotes:
#         for line in quotes:
#             if 'split' in line:
#                 await bot.say((line.replace('split', '')))
#
# @quote.command()
# async def thynnmas():
#     with open('quotes.txt', 'r') as quotes:
#         for line in quotes:
#             if 'thynnmas' in line:
#                 await bot.say((line.replace('thynnmas', '')))
#
# @quote.command()
# async def lester():
#     with open('quotes.txt', 'r') as quotes:
#         for line in quotes:
#             if 'lester' in line:
#                 await bot.say((line.replace('lester', '')))

with open('token.txt', 'r') as bot_token:
    token = bot_token.read()

client.run(token)






