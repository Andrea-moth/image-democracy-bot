import json
from discord.ext import commands
from rich.console import Console

debug = Console()

class reactor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        info = json.loads(open("./info.json").read())

        guildId = str(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        channelId = str(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        messageId = str(payload.message_id)

        if messageId not in info[guildId][channelId]:
            return

        for reaction in message.reactions:
            if payload.member in await reaction.users().flatten() and str(reaction) != str(payload.emoji):
                await message.remove_reaction(reaction.emoji, payload.member)
        
        if payload.emoji.name == "🔼":
            info[guildId][channelId][messageId]["score"] += 1
            debug.log(f"[green1][REACTION][/green1] [dark_violet]+1 to [blue]{info[guildId][channelId][messageId]['url']}[/blue][/dark_violet]")
        if payload.emoji.name == "🔽":
            info[guildId][channelId][messageId]["score"] -= 1
            debug.log(f"[green1][REACTION][/green1] [dark_violet]-1 to [blue]{info[guildId][channelId][messageId]['url']}[/blue][/dark_violet]")

        with open("./info.json", "w") as infoFile:
            json.dump(info, infoFile, indent=4)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        info = json.loads(open("./info.json").read())

        guildId = str(payload.guild_id)
        channelId = str(payload.channel_id)
        messageId = str(payload.message_id)

        if messageId not in info[guildId][channelId]:
            return
        
        if payload.emoji.name == "🔼":
            info[guildId][channelId][messageId]["score"] -= 1
            debug.log(f"[green1][REACTION][/green1] [dark_violet]-1 to [blue]{info[guildId][channelId][messageId]['url']}[/blue][/dark_violet]")
        if payload.emoji.name == "🔽":
            info[guildId][channelId][messageId]["score"] += 1
            debug.log(f"[green1][REACTION][/green1] [dark_violet]+1 to [blue]{info[guildId][channelId][messageId]['url']}[/blue][/dark_violet]")

        with open("./info.json", "w") as infoFile:
            json.dump(info, infoFile, indent=4)

def setup(bot):
    bot.add_cog(reactor(bot))