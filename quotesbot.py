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
     await bot.change_presence(game=discord.Game(name='Loading SkyNet'))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        with open('quotes.txt', 'r') as quoted_text:
            for line in quoted_text:
                if line.startswith(message.content):
                    await bot.send_message(message.channel, line.replace(message.content, ''))
                    break

    await bot.process_commands(message)

     

@bot.command()
async def roll(minroll: int, maxroll: int):
    randomint = random.randint(minroll, maxroll)
    await bot.say(randomint)

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def weather(country : str, city : str):
    with open('weatherapi.txt', 'r') as weather_key:
        api_key = weather_key.read()

    url = 'http://api.wunderground.com/api/' + api_key + '/geolookup/conditions/q/' + country + '/' + city + '.json'
    f = urllib.request.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    temp_c = parsed_json['current_observation']['temp_c']
    weather = parsed_json['current_observation']['weather']
    await bot.say("Current temperature in " + location + " is " + str(temp_c) + "C and the condition is " + weather)
    f.close()

@bot.command()
async def predict(*args):
    prediction = random.choice(args)
    await bot.say(prediction)

@bot.command()
async def changegame(gamename : str):
     await bot.change_presence(game=discord.Game(name=gamename))

@bot.command()
async def prizepool():
     prizepool = list(range(15000000, 25000000))
     prize_prediction = random.choice(prizepool)
     await bot.say("The prizepool will be: " + str(prize_prediction))

with open('token.txt', 'r') as bot_token:
    token = bot_token.read()

#client.run(token)

bot.run(token)







