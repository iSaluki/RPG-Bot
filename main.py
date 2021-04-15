import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import random
import requests

#Global Settings
prefix = ";"
version = "v0.1"

# API Test
url = "http://127.0.0.1:5000/post"

@slash.slash(name="move", description="Move your character in the game", options=[create_option(name="Direction", description="Provide a direction to move.", option_type=3, required=False)])
async def slash_move(ctx, *args):
    content ={
        "user": str(ctx.user.id),
        "command": "move",
        "args": args,
    }
    requests.post(url, json = content)

# Create bot
bot = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print("Logged in")
    activity = discord.Game(name="with a cool new game", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run("NzQ4OTM5MTQ0ODM0NTgwNDkw.X0kt7g.G8ewY4O9AvsoXuPGH42Jy6O9euM")
