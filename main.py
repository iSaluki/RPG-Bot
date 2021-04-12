import discord
from discord.ext import commands
import random
import asyncio
import time
import subprocess
prefix = ";"
version = "v0.1"
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Logged in")

@bot.command()
async def status(ctx):

    latency = str(bot.latency * 1000)[:7] + "ms"
    shard = "No shard detected" if str(bot.shard_id) == "None" else  str(bot.shard_id) + "/" + str(bot.shard_count)


    embed=discord.Embed(title="Status", description="Bot status information", color=0x06bc5e)
    embed.add_field(name="Latency", value=latency, inline=True)
    embed.add_field(name="Shard", value=shard, inline=True)
    embed.add_field(name="Version", value=version, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def map(ctx):
    async with ctx.typing():
        subprocess.run("node web.js", shell=True)
        #await time.sleep(2)
        
        with open("cache/map.png", "rb") as fh:
            f = discord.File(fh, filename="map.png")
        await ctx.send(file=f)

@bot.command()
async def stupid(ctx, *, content:str):
        stupidity = random.randint(0,1)
        if stupidity == 0:
            await ctx.send(content+ " isn't stupid")

        elif stupidity == 1:
            await ctx.send(content+ " is stupid")



bot.run("NzQ4OTM5MTQ0ODM0NTgwNDkw.X0kt7g.G8ewY4O9AvsoXuPGH42Jy6O9euM")