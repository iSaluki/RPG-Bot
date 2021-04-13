import discord
from discord.ext import commands
import random
import asyncio
import time
import subprocess



#Global Settings
prefix = ";"
version = "v0.1"
colour = 0x0ccfaf

bot = commands.Bot(command_prefix=prefix)



# Map Generation Variables
allowedButtons = ["sepia","grayscale","dingy","tint"]
allowedLayers = ["Texture","Height","Biomes","Cells",
                 "Grid","Coordinates","Compass","Rivers","Relief",
                 "Religions","Cultures","States","Provinces","Zones",
                 "Borders","Routes","Temp","Ice","Population",
                 "Prec","Emblems","Labels","Icons","Military",
                 "Markers","Rulers","ScaleBar"]

@bot.event
async def on_ready():
    print("Logged in")

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
    async with ctx.typing():
        invalidArg = False
        argsToGo = ""
        for arg in args:
            if arg.lower() in allowedButtons:
                argsToGo += "b"+arg.lower()+" "
            elif arg[0].upper()+arg[1:].lower() in allowedLayers:
                argsToGo += "l"+arg[0].upper()+arg[1:].lower()+" "
            else:
                invalidArg = True
        if not invalidArg:
            subprocess.run("node web.js "+argsToGo, shell=True)      
            #with open("cache/map.png", "rb") as fh:
                
                
            f = discord.File("cache/map.png", filename="image.png")           
            embed=discord.Embed(title=":map: | Map", color = colour)
            embed.set_image(url="attachment://image.png")
            embed.set_footer(text=":gear: | Settings: " + argsToGo)
            embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
            await ctx.send(file=f, embed=embed)
           
        else:
            await ctx.send("That's not a valid arg! Type "+prefix+"args for avaliable arguments")

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
