import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="info")
    async def _test(self, ctx):
        embed=discord.Embed(title="Info", description="About the bot", color=colour)
        embed.add_field(name=":tools: | Developer", value="Saluki#7350", inline=False)
        embed.add_field(name=":earth_africa: | Map Generation powered by", value="https://github.com/Azgaar/Fantasy-Map-Generator", inline=True)
        embed.add_field(name=":ringed_planet: | Testers", value="Chilledtiger999#9580", inline=False)
        embed.set_footer(text="Use "+prefix+"status to see more details")
        await ctx.send(embed=embed)
        await ctx.send(content="test", embeds=[embed])

def setup(bot):
    bot.add_cog(Status(bot))
