import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
import random
import asyncio
import time
import subprocess
import os


#Global Settings
prefix = ";"
version = "v0.1"
colour = 0x0ccfaf

bot = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)



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
    activity = discord.Game(name="For Maps", type=3)
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

@bot.command()
async def map(ctx, *args):
        #print("mapfunc: ",args[0])
        #args = args[0]
    async with ctx.typing():
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
            #with open("cache/map.png", "rb") as fh:
                
                
            f = discord.File("cache/"+filename+".png", filename="image.png")           
            embed=discord.Embed(title=":map: | Map", color = colour)
            embed.set_image(url="attachment://image.png")
            if argsToGo == "":
                 argsToGo = "None"
            embed.set_footer(text="Settings: " + argsToGo)
            #embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
            await ctx.send(file=f, embed=embed)
            os.remove("cache/"+filename+".png")
           
        else:
            if styleButtons >1:
                await ctx.send("You can only use one style at a time!")
            if invalidArg:
                await ctx.send(invalidArgs+"are not valid arguments. Type "+prefix+"args for avaliable arguments")

@slash.slash(name="map", description="Generate a fantasy map", options=[create_option(name="Settings", description="Add settings, seperated by spaces", option_type=3, required=False)])
async def slash_map(ctx, *args):
    print(args)
    await map(ctx, args)

@slash.slash(name="args", description="See all the settings for generating a fantasy map")
async def slash_args(ctx):
    await args(ctx)


@bot.command()
async def info(ctx):
    embed=discord.Embed(title="Info", description="About the bot", color=colour)
    embed.add_field(name=":tools: | Developer", value="Saluki#7350", inline=False)
    embed.add_field(name=":earth_africa: | Map Generation powered by", value="https://github.com/Azgaar/Fantasy-Map-Generator", inline=True)
    embed.add_field(name=":ringed_planet: | Testers", value="Chilledtiger999#9580", inline=False)
    embed.set_footer(text="Use "+prefix+"status to see more details")
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
async def stupid(ctx, *, content:str):
        stupidity = random.randint(0,1)
        if stupidity == 0:
            await ctx.send(content+ " isn't stupid")

        elif stupidity == 1:
            await ctx.send(content+ " is stupid")



bot.run("NzQ4OTM5MTQ0ODM0NTgwNDkw.X0kt7g.G8ewY4O9AvsoXuPGH42Jy6O9euM")
