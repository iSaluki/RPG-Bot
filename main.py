import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import random
import requests
import os
import json
from time import asctime
import logging
import datetime

logging.basicConfig(filename="bot.log", level=logging.DEBUG)

prefix = ";"
version = "v0.1.1"
PRODUCTION = True
COLOUR = 0x0fb1b3
SHARDING = False

authToken = "Your own token that corresponds to the one you set on the API"

# Emojis
x_emoji = "<:X_:833700097903689728>"


if PRODUCTION:
    domain = "https://production-api-address.com/api"
    token = "Production bot token"
else:
    #domain = "http://0.0.0.0:8080/api"
    domain = "https://testing-api-address.com/api"
    token = "Testing bot token"

# API Config
geturl = domain + "/get"
posturl = domain + "/post"

# Create bot

if SHARDING:
    BotType = commands.AutoShardedBot
    #,shard_count=8, shard_ids=[0, 1, 2, 3]
else:
    BotType = commands.Bot

bot = BotType(command_prefix=prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


async def ConstructEmbed(reply, cmdName, ctx):
    cmdName = cmdName.capitalize()
    logging.debug(f"{asctime()} EMBED: reply is: ", reply)
    embed=discord.Embed(title=cmdName,description=reply, color=COLOUR)
    embed.timestamp = datetime.datetime.utcnow()

    return embed
    logging.debug(f"{asctime()} EMBED: Returning embed variable: ", embed)


@bot.event
async def on_ready():
    logging.debug(f"{asctime()} LOGIN: Bot has logged in")
    activity = discord.Game(name="/help", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    logging.debug(f"{asctime()} LOGIN: Status updated")


@slash.slash(name="bstat", description="Get bot information")
async def slash_bstat(ctx):

    shard = "Not sharded" if str(bot.shard_id) == "None" else  str(bot.shard_id) + "/" + str(bot.shard_count)
    latency = str(bot.latency * 1000)[:3] + "ms"

    embed=discord.Embed(title="Bot Stats", description="Basic information about the bot status", color=COLOUR)
    embed.add_field(name="Shard", value=shard, inline=True)
    embed.add_field(name="Latency", value=latency, inline=True)
    embed.add_field(name="Version", value=version, inline=True)
    await ctx.send(embed=embed)


# Yet to be implemented
@slash.slash(name="buy", description="Buy something from a vendor with money", options=[create_option(name="Item", description="The item you want to buy", option_type=3, required=True)])
async def slash_buy(ctx, item):

    content ={
        "user": str(ctx.author_id),
        "command": "buy",
        "args": item,
    }
    logging.debug(f"{asctime()} SLASH_BUY: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


@slash.slash(name="drop", description="Drop an item at your current location", options=[create_option(name="Item", description="The item you want to drop", option_type=3, required=True)])
async def slash_drop(ctx, item):

    content ={
        "user": str(ctx.author_id),
        "command": "drop",
        "args": item,
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


@slash.slash(name="pickup", description="Pickup a nearby object", options=[create_option(name="Item", description="The item you want to pickup", option_type=3, required=True)])
async def slash_pickup(ctx, item):

    content ={
        "user": str(ctx.author_id),
        "command": "pickup",
        "args": item,
    }
    logging.debug(f"{asctime()} SLASH_PICKUP: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


@slash.slash(name="help", description="Get help")
async def slash_help(ctx):
    
    embed=discord.Embed(title="Help",description="If you need help with the bot or the game, please look at the options below!", color=COLOUR)
    embed.add_field(name="Support Server", value="[Join here](https://discord.gg/aq37JpbZpR)")
    embed.add_field(name="Technical or Billing support", value="Contact Saluki#7350 or seth@salukicorporation.com")
    embed.add_field(name="Suggestions and bug reports", value="See the #feedback channel in the support server")
    embed.set_footer(text="If you're unsure which option is right for you, join the support server and ask there.")
    embed.timestamp = datetime.datetime.utcnow()
    #embed = await ConstructEmbed(reply, cmdName, ctx)
    await ctx.send(embed=embed)


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
@slash.slash(name="sell", description="Sell your items to a vendor", options=[create_option(name="Item", description="The item you want to sell", option_type=3, required=True)])
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
@slash.slash(name="use", description="Use an item from your inventory",options=[create_option(name="Item", description="The item you want to use", option_type=3, required=True)])
async def slash_use(ctx, item):

    content ={
        "user": str(ctx.author_id),
        "command": "use",
        "args": item,
    }
    logging.debug(f"{asctime()} SLASH_USE: content = {content}")
    await ctx.defer()
    await send_post(ctx, content)


async def send_post(ctx, to_send):
    AuthHeader = {'Authentication': authToken}
    response = requests.post(posturl, json = to_send, headers=AuthHeader)
    received = json.loads(response.content)
    logging.debug(f"{asctime()} SEND_POST: received = {received}")
    if to_send["command"]==received["command"]:
        if "args" not in to_send or to_send["args"][0]==received["args"][0]:
            logging.debug(f"{asctime()} SEND_POST: SUCCESS reply = {received['reply']}")
            reply = received["reply"]
            cmdName = received["command"]
            embed = await ConstructEmbed(reply, cmdName, ctx)
            await ctx.send(embed=embed)
        else:
            logging.warning(f"{asctime()} SEND_POST: API ERROR args returned do not match args sent")
            await ctx.send("API error. If this happens a lot, please report it.")
    else:
        logging.warning(f"{asctime()} SEND_POST: API ERROR command returned does not match command sent")
        await ctx.send("API error. If this happens a lot, please report it.")


bot.run(token)
