import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import random
import requests
import json

#Global Settings
prefix = ";"
version = "v0.1"

PRODUCTION = True

if PRODUCTION:
    domain = "https://rpg-bot-6ptoc.ondigitalocean.app"
    token = "ODMzMjU2Njk4ODM4Nzc3ODg2.YHvsxg.PdcTHAVtQzlqRb2-hCBZUHL_0CA"
else:
    domain = "http://localhost:8080"
    token = "NzQ4OTM5MTQ0ODM0NTgwNDkw.X0kt7g.G8ewY4O9AvsoXuPGH42Jy6O9euM"

# API Config
geturl = domain + "/get"
posturl = domain + "/post"

# Create bot
bot = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print("Logged in")
    activity = discord.Game(name="try /move", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@slash.slash(name="move", description="Move your character in the game", options=[create_option(name="Direction", description="Provide a direction to move.", option_type=3, required=True)])
async def slash_move(ctx, direction):

    content ={
        "user": str(ctx.author_id),
        "command": "move",
        "args": direction,
    }
    await send_post(ctx, content)
    
    #newStatus = requests.get(geturl, params={"user":str(ctx.author_id)})
    #await ctx.send(str(newStatus.content, "UTF-8"))

async def send_post(ctx, toSend):
    response = requests.post(posturl, json = toSend)
    received = json.loads(response.content)
    print(received)
    if toSend["command"]==received["command"] and toSend["args"][0]==received["args"][0]:
        await ctx.send(received["reply"])
    else:
        await ctx.send("API error")


bot.run(token)