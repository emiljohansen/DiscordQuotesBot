import discord, asyncio, random, re, signal, string
import urllib.request, json, pickle
import operator
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description='Reacts to given commands, use !help for list of available commands')

wordcount_dict = {}

regex = re.compile('[%s]' % re.escape(string.punctuation))

excluded_words = ['the', 'to', 'of', 'a', 'an', 'in', 'and', 'i', 'it', 'that', 'his', 'hers', 'you', 'I']

@bot.event
async def on_ready():
     print('Logged in as')
     print(bot.user.name)
     print(bot.user.id)
     print('----')
     global wordcount_dict
     wordcount_dict = pickle.load(open("wordcount.p", "rb"))
     print(str(wordcount_dict))
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

    await bot.process_commands(message)

    if not message.content.startswith('!'):
        for words in message.content.split():
            clean_words = regex.sub('', words)
            #print(clean_words)
            if clean_words not in excluded_words:
                if clean_words in wordcount_dict:
                    wordcount_dict[clean_words] += 1
                else:
                    wordcount_dict[clean_words] = 1

    write_dict_to_file(wordcount_dict)

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#
#     if not message.content.startswith('!'):
#         for words in message.content.split():
#             clean_words = regex.sub('', words)
#             #print(clean_words)
#             if clean_words in wordcount_dict:
#                 wordcount_dict[clean_words] += 1
#             else:
#                 wordcount_dict[clean_words] = 1
#
#     write_dict_to_file(wordcount_dict)



@bot.command()
async def roll(minroll: int, maxroll: int):
    """Rolls a random number between the two numbers given as parameters"""
    randomint = random.randint(minroll, maxroll)
    await bot.say(randomint)

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def weather(city : str, country : str):
    """Outputs the weather given a city and a country seperated by space."""
    with open('weatherapi.txt', 'r') as weather_key:
        api_key = weather_key.read()

    url = 'http://api.wunderground.com/api/' + api_key + '/geolookup/conditions/q/' + country + '/' + city + '.json'
    f = urllib.request.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    temp_c = parsed_json['current_observation']['temp_c']
    weather = parsed_json['current_observation']['weather']
    await bot.say("Current temperature in " + location + " is " + str(temp_c) + "C and the conditions are " + weather)
    f.close()

@bot.command()
async def wordcount():
    """Displays the 5 most common words said in this server"""
    sorted_words = sorted(wordcount_dict.items(), key = operator.itemgetter(1), reverse = True)
    response = ""
    print(sorted_words)
    for i in range(5):
       response += str(sorted_words[i]) + "\n"

    await bot.say(response)

@bot.command()
async def predict(*args):
    """Predicts a random option of an arbitrary list of things"""
    prediction = random.choice(args)
    await bot.say(prediction)

@bot.command()
async def changegame(gamename : str):
    """Changes the bots playing message"""
    await bot.change_presence(game=discord.Game(name=gamename))

@bot.command()
async def prizepool():
    """Predicts the prizepool for TI7"""
    prizepool = list(range(15000000, 25000000))
    prize_prediction = random.choice(prizepool)
    await bot.say("The prizepool will be: " + str(prize_prediction))


def write_dict_to_file(dict):
    pickle.dump(dict, open("wordcount.p", "wb"))


with open('token.txt', 'r') as bot_token:
    token = bot_token.read()

#client.run(token)

bot.run(token)