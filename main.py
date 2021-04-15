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

# API Test
url = "http://127.0.0.1:5000/post"

# Create bot
bot = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print("Logged in")
    activity = discord.Game(name="with a cool new game", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@slash.slash(name="move", description="Move your character in the game", options=[create_option(name="Direction", description="Provide a direction to move.", option_type=3, required=False)], guild_ids=[697477880938102925])
async def slash_move(ctx, *args):

    content ={
        "user": str(ctx.author_id),
        "command": "move",
        "args": args,
    }
    response = requests.post(url, json = content)
    print(response.content)
    content = json.loads(response.content)
    print(content)
    print(content["args"], content["args"][0], args[0])
    if content["command"]=="move" and content["args"][0]==args[0]:
        await ctx.send("OK")
    else:
        await ctx.send("API error")

bot.run("NzQ4OTM5MTQ0ODM0NTgwNDkw.X0kt7g.G8ewY4O9AvsoXuPGH42Jy6O9euM")
