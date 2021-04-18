import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import random
import requests
import json
from time import asctime
import logging

logging.basicConfig(filename="bot.log", level=logging.DEBUG)
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
    logging.debug(f"{asctime()} SLASH_MOVE: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


async def send_post(ctx, to_send):
    response = requests.post(posturl, json = to_send)
    received = json.loads(response.content)
    logging.debug(f"{asctime()} SEND_POST: received = {received}")
    if to_send["command"]==received["command"] and to_send["args"][0]==received["args"][0]:
        logging.debug(f"{asctime()} SEND_POST: SUCCESS reply = {received['reply']}")
        await ctx.send(received["reply"])
    else:
        logging.debug(f"{asctime()} SEND_POST: API ERROR")
        await ctx.send("API error")


bot.run(token)