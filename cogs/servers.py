import json
from turtle import title
import discord
from discord_slash import cog_ext
from discord.ext import commands
from rich.console import Console

debug = Console()

class reactor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        info = json.loads(open("./info.json").read())

        if str(guild.id) in info:
            return

        info.update({str(guild.id):{}})

        debug.log(f"[green1][JOINED][/green1] [dark_violet]I have joined {guild.name}")
        
        with open("./info.json", "w") as infoFile:
            json.dump(info, infoFile, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        info = json.loads(open("./info.json").read())
        
        if str(guild.id) not in info:
            return

        del info[str(guild.id)]

        debug.log(f"[green1][LEFT][/green1] [dark_violet]I have left {guild.name}")

        with open("./info.json", "w") as infoFile:
            json.dump(info, infoFile, indent=4)

    @commands.command()
    async def config(self, ctx):
        info = json.loads(open("./info.json").read())

        channels = []
        for num, channel in enumerate(info[str(ctx.guild.id)], 1):
            channelName = ctx.guild.get_channel(int(channel))
            channels.append(" - ".join([str(num), str(channelName)]))
        channels = "\n".join(channels)
        if not channels:
            channels = "No channels have been setup"

        configMessage = discord.Embed(
            title="CONFIG",
            description=f"Configure the image channels",
            color=0xA30262
        )
        configMessage.add_field(
            name="Channels",
            value=f"{channels}"
        )
        
        await ctx.send(embed=configMessage)

def setup(bot):
    bot.add_cog(reactor(bot))