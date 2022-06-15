import discord, os
from discord_slash import SlashCommand
from rich.console import Console
from rich.progress import Progress
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="+", intents=intents)
slash = SlashCommand(bot, sync_commands=True)

debug = Console()
token = "OTgzOTg4NzkyMDkwMzI5MTY5.GdlhWG.xYanMfTJF8kG9E6pSVg6FIhOe9WIpp96EQhTO8"

async def loadCogs():
    with Progress() as cogLoading:
        loading = cogLoading.add_task("[green1]Loading cogs...", total=100)

        while not cogLoading.finished:
            cogs = [cog[:-3] for cog in os.listdir("./cogs") if cog.endswith(".py")]
            for cog in cogs:
                try:
                    bot.load_extension(f"cogs.{cog}")
                except commands.errors.NoEntryPointError:
                    debug.log(f"[red][ERROR][/red] [dark_violet]{cog} was not able to be loaded")
                cogLoading.update(loading, advance=(100/len(cogs)))
                
@bot.event
async def on_ready():
    debug.rule(f"[green1][Start]", style="dark_violet", align="left")

    await loadCogs()

    debug.log(f"[green1][STARTUP][/green1] [dark_violet]{bot.user} connected")

if __name__ == "__main__":
    bot.run(token)  
