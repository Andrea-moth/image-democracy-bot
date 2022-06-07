import json
import discord
from discord.ext import commands
from rich.console import Console

debug = Console()

class reactor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #checks for someone adding a reaction
    #adds score appropriatly 
    #does nothing if in the wrong channel or a bot reacts
    #does not allow multiple reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        info = json.loads(open("./info.json").read())
        msgId = str(payload.message_id)
        chnl = await self.bot.fetch_channel(payload.channel_id)
        msg = await chnl.fetch_message(msgId)

        if payload.member.bot:
            return
        if msgId not in list(info["images"].keys()):
            return

        
        if payload.emoji.name == "🔼":
            debug.log(f"[green1][REACTION][/green1] [dark_violet]+1 to [blue]{info['images'][msgId]['img']}[/blue][/dark_violet]")
            info["images"][msgId]["score"] += 1
        if payload.emoji.name == "🔽":
            debug.log(f"[green1][REACTION][/green1] [dark_violet]-1 to [blue]{info['images'][msgId]['img']}[/blue][/dark_violet]")
            info["images"][msgId]["score"] -= 1
        for reaction in msg.reactions:
            if payload.member in await reaction.users().flatten() and str(reaction) != str(payload.emoji):
                await msg.remove_reaction(reaction.emoji, payload.member)


        with open("./info.json", "w") as infoFile:
                infoFile.seek(0)
                json.dump(info, infoFile, indent=4)
    
    #checks for someone removing a reaction
    #adds/subtracts the score appropriatly
    #does nothing if not in the correct channel or if it's a bot reacting
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        info = json.loads(open("./info.json").read())
        message = str(payload.message_id)

        if payload.user_id == self.bot.user.id:
            return
        if str(message) not in list(info["images"].keys()):
            return
        
        if payload.emoji.name == "🔼":
            debug.log(f"[green1][REACTION][/green1] [dark_violet]-1 to [blue]{info['images'][message]['img']}[/blue][/dark_violet]")
            info["images"][message]["score"] -= 1
        if payload.emoji.name == "🔽":
            debug.log(f"[green1][REACTION][/green1] [dark_violet]+1 to [blue]{info['images'][message]['img']}[/blue][/dark_violet]")
            info["images"][message]["score"] += 1


        with open("./info.json", "w") as infoFile:
            infoFile.seek(0)
            json.dump(info, infoFile, indent=4)

def setup(bot):
    bot.add_cog(reactor(bot))
