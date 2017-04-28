import discord, asyncio, random, re
import urllib.request, json
from discord.ext import commands

#client = discord.Client()

bot = commands.Bot(command_prefix='!', description='This bot responds to commands with a quote... for now')

# @client.event
# async def on_ready():
#     print('Logged in as')
#     print(client.user.name)
#     print(client.user.id)
#     print('------')
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('!'):
#         with open('quotes.txt', 'r') as quoted_text:
#             for line in quoted_text:
#                 if line.startswith(message.content):
#                     msg = line
#                     await client.send_message(message.channel, line.replace(str(message.content), ''))

@bot.event
async def on_ready():
     print('Logged in as')
     print(bot.user.name)
     print(bot.user.id)
     print('----')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if message.content.startswith('!'):
        with open('quotes.txt', 'r') as quoted_text:
            for line in quoted_text:
                if line.startswith(message.content):
                    await bot.send_message(message.channel, line.replace(message.content, ''))

@bot.command()
async def roll(minroll: int, maxroll: int):
    randomint = random.randint(minroll, maxroll)
    await bot.say(randomint)

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def weather():
    url = 'http://api.wunderground.com/api/-APIKEY-/geolookup/conditions/q/France/Paris.json'
    f = urllib.request.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    temp_f = parsed_json['current_observation']['temp_f']
    await bot.say('Current temperature in ' + location + 'is ' + temp_f)
    f.close()
#with open('token.txt', 'r') as bot_token:
#    token = bot_token.read()

#client.run(token)

bot.run(token)






