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
COLOUR = 0x0fb1b3
SHARDING = True



# Emojis

x_emoji = "<:X_:833700097903689728>"


if PRODUCTION:
    domain = "https://rpg-bot-6ptoc.ondigitalocean.app/api"
    token = "ODMzMjU2Njk4ODM4Nzc3ODg2.YHvsxg.PdcTHAVtQzlqRb2-hCBZUHL_0CA"
else:
    domain = "http://0.0.0.0:8080/api"
    token = "NzQ4OTM5MTQ0ODM0NTgwNDkw.X0kt7g.G8ewY4O9AvsoXuPGH42Jy6O9euM"

# API Config
geturl = domain + "/get"
posturl = domain + "/post"

# Create bot

if SHARDING:
    BotType = commands.AutoShardedBot
else:
    BotType = commands.Bot

bot = BotType(command_prefix=prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("Logged in")
    activity = discord.Game(name="/help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@slash.slash(name="bstat", description="Get bot information")
async def slash_bstat(ctx):

    shard = "No shard detected" if str(bot.shard_id) == "None" else  str(bot.shard_id) + "/" + str(bot.shard_count)
    latency = str(bot.latency * 1000)[:7] + "ms"

    embed=discord.Embed(title="Bot Stats", description="Basic information about the bot status", color=COLOUR)
    embed.add_field(name="Shard", value=shard, inline=True)
    embed.add_field(name="Latency", value=latency, inline=True)
    embed.add_field(name="Version", value=version, inline=True)
    await ctx.send(embed=embed)

# Yet to be implemented
@slash.slash(name="buy", description="Buy something from a vendor with money", options=[create_option(name="item", description="The item you want to buy", option_type=3, required=True)])
async def slash_buy(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "buy",
    }
    logging.debug(f"{asctime()} SLASH_BUY: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


# Yet to be implemented
@slash.slash(name="drop", description="Drop an item at your current location")
async def slash_drop(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "drop",
    }
    logging.debug(f"{asctime()} SLASH_DROP: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


# Yet to be implemented
@slash.slash(name="fight", description="Fight a monster ,a player ...or something else")
async def slash_fight(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "fight",
    }
    logging.debug(f"{asctime()} SLASH_FIGHT: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


# Yet to be implemented
@slash.slash(name="get", description="Pick up a nearby object")
async def slash_get(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "get",
    }
    logging.debug(f"{asctime()} SLASH_GET: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


@slash.slash(name="help", description="Provide help printout for commands and the game")
async def slash_help(ctx):
    await ctx.send(x_emoji+"This menu is currently in development and will be functional soon. For now, please just use slash commands. Start a message with a `/` and then pick a command from the list. Message Saluki#7350 for more help.")


# Yet to be implemented
@slash.slash(name="inventory", description="Show your inventory")
async def slash_inventory(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "inventory",
    }
    logging.debug(f"{asctime()} SLASH_INVENTORY: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


@slash.slash(name="location", description="Get details about your current location")
async def slash_location(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "location",
    }
    logging.debug(f"{asctime()} SLASH_LOCATION: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


@slash.slash(name="move", description="Move to a different location", options=[create_option(name="Direction", description="Provide a direction to move.", option_type=3, required=True)])
async def slash_move(ctx, direction):

    content ={
        "user": str(ctx.author_id),
        "command": "move",
        "args": direction,
    }
    logging.debug(f"{asctime()} SLASH_MOVE: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


# Yet to be implemented
@slash.slash(name="open", description="Open something, might require a key")
async def slash_open(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "open",
    }
    logging.debug(f"{asctime()} SLASH_OPEN: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


# Yet to be implemented
@slash.slash(name="sell", description="Sell your items to a vendor", options=[create_option(name="item", description="The item you want to sell", option_type=3, required=True)])
async def slash_sell(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "sell",
    }
    logging.debug(f"{asctime()} SLASH_SELL: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


# Yet to be implemented
@slash.slash(name="trade", description="Trade with a player or vendor")
async def slash_trade(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "trade",
    }
    logging.debug(f"{asctime()} SLASH_TRADE: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


# Yet to be implemented
@slash.slash(name="use", description="Use an item from your inventory",options=[create_option(name="item", description="The item you want to use", option_type=3, required=True)])
async def slash_use(ctx):

    content ={
        "user": str(ctx.author_id),
        "command": "use",
    }
    logging.debug(f"{asctime()} SLASH_USE: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


async def send_post(ctx, to_send):
    response = requests.post(posturl, json = to_send)
    received = json.loads(response.content)
    logging.debug(f"{asctime()} SEND_POST: received = {received}")
    if to_send["command"]==received["command"]:
        if "args" not in to_send or to_send["args"][0]==received["args"][0]:
            logging.debug(f"{asctime()} SEND_POST: SUCCESS reply = {received['reply']}")
            await ctx.send(received["reply"])
        else:
            logging.warning(f"{asctime()} SEND_POST: API ERROR args returned do not match args sent")
            await ctx.send("API error. If this happens a lot, please report it.")
    else:
        logging.warning(f"{asctime()} SEND_POST: API ERROR command returned does not match command sent")
        await ctx.send("API error. If this happens a lot, please report it.")


bot.run(token)
