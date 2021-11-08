import os
import discord
from discord.ext import commands, tasks
from random import choice
import requests  #allows code to make HTTP requests from API
import json
from keep_alive import keep_alive
from main_cog import main_cog
from music_cog import music_cog

status = ['Running Harvests Farming Operations!']  #array for statuses

bot = commands.Bot(command_prefix='!')  #Setting prefix for commands

#remove the default help command so that we can write out own
bot.remove_command('help')

#register the class with the bot
bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))

@tasks.loop(seconds=60)  #looping through array every 20 seconds
async def change_status():
  await bot.change_presence(activity=discord.Game(choice(status)))


@bot.command(name='motivate', help='Test my abilities with a motivational quote.')
async def motivational_quote(ctx):  #printing motivational quotes
  response = requests.get("https://zenquotes.io/api/random")  #pulling quote from API
  json_data = json.loads(response.text)  #assigning JSON data to response variable
  quote = json_data[0]['q'] + " - " + json_data[0]['a']  #formatting quote for readability
  await ctx.send(quote)  #outputting quote to discord


@bot.command(name='hello', help="Say hello, I wasn't programmed to bite yet.")
async def greeting(ctx):
  responses = ['Hello.', 'How are you today?', 'Greetings.']
  await ctx.send(choice(responses))


@bot.command(name='goodbye', help="Say goodbye, glad I could be of service.")
async def parting(ctx):
  response = ['Goodbye.', 'Glad I could be of service.']
  await ctx.send(choice(response))


@bot.command(name='credits', help='Learn more about my creator.')
async def credits(ctx):
  await ctx.send('After much coffee and research, I was programmed by Matthew Hirmiz. My creator and I share a birthday, as I was put into service effective May 24, 2021.')


@bot.command(name='ping', help='How is our connection?')
async def ping(ctx):
  await ctx.send(f'**Pong** : {round(bot.latency * 1000)}ms')


async def join(ctx, voice):
  channel = ctx.author.voice.channel

  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect()


def mockify(normalText):
  mockText = ''

  for index, letter in enumerate(normalText.lower(), start=0):
    if index % 2 == 0:
      mockText += letter
    else:
      mockText += letter.upper()
      return mockText


@bot.command(name='mock', help="You're being insulted, human")
async def mock(ctx, *, message=None):
  # Delete the invocation message so it looks like the bot is saying this of its own accord
  await discord.Message.delete(ctx.message)

  # If they did not specify a message, send one of my favorite gifs instead
  if not message:
    await ctx.send('https://tenor.com/view/oh-fuck-off-go-away-just-go-leave-me-alone-spicy-wings-gif-14523970')
    # Otherwise, mock them
  else:
    await ctx.send(mockify(message))


@bot.command(name='clear', help='Clear a certain amount of messages from a channel.')
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)
  await ctx.send('https://tenor.com/view/thanos-gone-reduced-to-atoms-end-game-infinity-war-gif-15573921')

r = requests.head(url="https://discord.com/api/v1")
try:
    print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("No rate limit")
@bot.event
async def on_ready():
    change_status.start()  #changing status
    print('{0.user} is online.'.format(bot))

keep_alive() #runs webserver
bot.run(os.getenv('BOT_TOKEN'))
