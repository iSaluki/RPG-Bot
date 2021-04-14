import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, remove_all_commands
import random
import asyncio
import time
import datetime
import subprocess
import os
import shutil


#Clear cache
shutil.rmtree('cache')
os.mkdir('cache')
print ("Cache cleared")

#Global Settings
prefix = ";"
version = "v0.1"
colour = 0x0ccfaf
bot_owner = 183240527649570816

# Create bot

bot = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

# Load cogs
#bot.load_extension("status.py")


# Map Generation Variables
allowedButtons = ["sepia","grayscale","dingy","tint"]
allowedLayers = ["Texture","Height","Biomes","Cells",
                 "Grid","Coordinates","Compass","Rivers","Relief",
                 "Religions","Cultures","States","Provinces","Zones",
                 "Borders","Routes","Temp","Ice","Population",
                 "Prec","Emblems","Labels","Icons","Military",
                 "Markers","Rulers","Scalebar"]

@bot.event
async def on_ready():
    print("Logged in")
    activity = discord.Game(name="with maps", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def status(ctx):

    latency = str(bot.latency * 1000)[:7] + "ms"
    shard = "No shard detected" if str(bot.shard_id) == "None" else  str(bot.shard_id) + "/" + str(bot.shard_count)


    embed=discord.Embed(title="Status", description="Bot status information", color=colour)
    embed.add_field(name="Latency", value=latency, inline=True)
    embed.add_field(name="Shard", value=shard, inline=True)
    embed.add_field(name="Version", value=version, inline=True)
    await ctx.send(embed=embed)

async def mapping(ctx, args):
    print("Mapping:", args)
    invalidArg = False
    argsToGo = ""
    invalidArgs = ""
    styleButtons = 0
    for arg in args:
        if arg.lower() in allowedButtons:
            argsToGo += "b"+arg.lower()+" "
            styleButtons += 1
        elif arg[0].upper()+arg[1:].lower() in allowedLayers:
            if arg.lower() == "scalebar":
                argsToGo += "ScaleBar"
            else:
                argsToGo += "l"+arg[0].upper()+arg[1:].lower()+" "
        else:
            invalidArg = True
            invalidArgs += arg +" "
    if not invalidArg and styleButtons <=1:
        filename = "map" + str(ctx.author.id) + str(random.randint(0,1000))
        subprocess.run("node web.js "+filename+" " + argsToGo, shell=True)      

        f = discord.File("cache/"+filename+".png", filename="image.png")           
        embed=discord.Embed(title=":map: | Map", color = colour)
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=f, embed=embed)
        os.remove("cache/"+filename+".png")
        #embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        
    else:
        if styleButtons >1:
            await ctx.send("You can only use one style at a time!")
        if invalidArg:
            await ctx.send(invalidArgs+"are not valid arguments. Type "+prefix+"args for avaliable arguments")

@bot.command()
async def map(ctx, *args):
    #print("mapfunc: ",args)
    #if len(args)>0:
    #    args = args[0]
    async with ctx.typing():
        await mapping(ctx, args)

@slash.slash(name="map", description="Generate a fantasy map", options=[create_option(name="Settings", description="Add settings, seperated by spaces", option_type=3, required=False)])
async def slash_map(ctx, *args):
    #print("Bob",args)
    if len(args)>0:
        #print("Brian",args[0].split())
        await ctx.defer()
        await mapping(ctx, args[0].split())
    else:
        await ctx.defer()
        await mapping(ctx, [])

@slash.slash(name="push",description="Push someone!",options=[create_option(name="User", description="The user you want to push", option_type=6, required=True)])
async def slash_push(ctx,user):
    await push(ctx,user)
@slash.slash(name="args", description="See all the settings for generating a fantasy map")
async def slash_args(ctx):
    await args(ctx)

@slash.slash(name="info", description="See information about how the bot was made")
async def slash_info(ctx):
    await info(ctx)

@slash.slash(name="status", description="See the status of the bot and debug information")
async def slash_status(ctx):
    await status(ctx)

@bot.command()
@commands.is_owner()
async def setstatus(ctx, args):
    activity = discord.Game(name=args, type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await ctx.send("Status updated to "+arg1)

@bot.command()
async def info(ctx):
    embed=discord.Embed(title="Info", description="About the bot", color=colour)
    embed.add_field(name=":tools: | Developer", value="Saluki#7350", inline=False)
    embed.add_field(name=":earth_africa: | Map Engine", value="https://github.com/Azgaar/Fantasy-Map-Generator", inline=True)
    embed.add_field(name=":ringed_planet: | Testers", value="Chilledtiger999#9580", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def args(ctx):
    embed=discord.Embed(title="Allowed Arguments", color=colour)
    buttons = ""
    for button in allowedButtons:
        buttons+=button[0].upper()+button[1:]+", "
    buttons = buttons[:-2]

    layers = ""
    for layer in allowedLayers:
        layers+=layer+", "
    layers = layers[:-2]
    embed.add_field(name="Filters", value=buttons, inline=False)
    embed.add_field(name="Layers", value=layers, inline=False)
    embed.set_footer(text="Use any of these after the map command")
    await ctx.send(embed=embed)

@bot.command()
async def push(ctx, user):
        balance = random.randint(0,1)
        if balance == 0:
            response = random.randint(0,5)
            if response == 0:
                balancetext = "dodged your push!"
            if response == 1:
                balancetext = "backfliped over you and evaded your push!"
            if response == 2:
                balancetext = "anticipated your move and pushed you over instead!"
            if response == 3:
                balancetext = "threw their shoe at you, causing you to fall over!"
            if response == 4:
                balancetext = "ran after you with a stick!"
            if response == 5:
                balancetext = "vaulted over you, dabbing as they did it!"
            await ctx.send(user.name+ " "+balancetext)

        elif balance == 1:
            response = random.randint(0,5)
            if response == 0:
                falltext = "has fallen and cannot get up!"
            if response == 1:
                falltext = "tried to block your push, but was too slow!"
            if response == 2:
                falltext = "fell into a bush!"
            if response == 3:
                falltext = "jumped over a cow to try and escape, but fell into a cow pat!"
            if response == 4:
                falltext = "didn't see you coming and fell right over!"
            if response == 5:
                falltext = "fell over, dropping your birthday cake, should have thought that one through!"
            await ctx.send(user.name+" "+ falltext)



bot.run("NzQ4OTM5MTQ0ODM0NTgwNDkw.X0kt7g.G8ewY4O9AvsoXuPGH42Jy6O9euM")
