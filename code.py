import discord, os, json
from rich.console import Console
from rich.progress import Progress
from discord.ext import commands

#variables needed for run time
intents = discord.Intents.default()
intents.members = True

botId = ""
bot = commands.Bot(command_prefix="+", intents=intents)
debug = Console()

#checks info file
#creates on if none available
try:
    info = json.loads(open("./info.json").read())
except FileNotFoundError:
    with open("./info.json", "w") as infoFile:
        info = {"channels": [], "images":{}}
        infoFile.seek(0)
        json.dump(info, infoFile, indent=4)

#loads all the cogs
#now with fancy bar
async def loadCogs():
    with Progress() as cogLoading:
        loading = cogLoading.add_task("[green1]Loading cogs...", total=100)
        notLoadedCogs = []

        while not cogLoading.finished:
            #gets all files in ./cogs ending in .py and strips the .py
            #then loads them with error checking
            cogs = [cog for cog in os.listdir("./cogs") if cog.endswith(".py")]
            for cog in cogs:
                try:
                    bot.load_extension(f"cogs.{cog[:-3]}")
                except commands.errors.NoEntryPointError:
                    notLoadedCogs.append(f"cogs.{cog[:-3]}")
                cogLoading.update(loading, advance=(100/len(cogs)))

        return notLoadedCogs

#checks all message ids in info file
#if it can't find the message it deletes them so as to save space
async def checkMessages():
    with Progress() as removeDeadMessages:
        checkMessages = removeDeadMessages.add_task("[green1]Checking stored message ids...", total=100)
        removeMessages = removeDeadMessages.add_task("[green1]Removing dead messages..", total=100)
        lostMessages = []
        ids = list(info["images"].keys())

        while not removeDeadMessages.finished:
            #finds all message ids
            #then tries to load them with error checking
            for channel in info["channels"]:
                chnl = bot.get_channel(channel)
                for msgId in ids:
                    try:
                        await chnl.fetch_message(str(msgId))
                    except discord.errors.NotFound:
                        lostMessages.append(msgId)
                try:
                    removeDeadMessages.update(checkMessages, advance=(100/len(ids)))
                except ZeroDivisionError:
                    removeDeadMessages.update(checkMessages, advance=100)
            
            #finally removes all the lost messages all at once to avoid file errors
            if not lostMessages:
                removeDeadMessages.update(removeMessages, advance=100)
            for lost in lostMessages:
                del info["images"][lost]
                removeDeadMessages.update(removeMessages, advance=(100/len(lostMessages)))                   

#loads cogs, checks the info file and starts the logging
@bot.event
async def on_ready():
    notLoaded = await loadCogs()
    await checkMessages()

    with open("./info.json", "w") as infoFile:
        infoFile.seek(0)
        json.dump(info, infoFile, indent=4)

    os.system("cls")
    
    debug.rule("[green1][Start]", style="dark_violet", align="left")
    
    if notLoaded:
        debug.log(f"[red][ERROR][/red] [dark_violet]{', '.join(notLoaded)} were not able to be loaded")

    debug.log(f"[green1][STARTUP][/green1] [dark_violet]{bot.user} connected")

bot.run(botId)
