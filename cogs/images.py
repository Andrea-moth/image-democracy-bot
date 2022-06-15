import json
import re
from discord.ext import commands
from rich.console import Console

debug = Console()

class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def reportMessage(self, message):
        info = json.loads(open("./info.json").read())
        guildId = str(message.guild.id)
        channelId = str(message.channel.id)
        referencedMessage = str(message.reference.message_id)

        await message.delete()

        if referencedMessage not in info[guildId][channelId]:
            return
        if message.author.id in info[guildId][channelId][referencedMessage]["reports"]:
            return
        if len(info[guildId][channelId][referencedMessage]["reports"]) > 10:
            channel = self.bot.get_channel(int(channelId))
            removeMessage = await channel.fetch_message(referencedMessage)
            await removeMessage.delete()
            debug.log(f"[green1][REPORT][green1] [dark_violet]{referencedMessage} removed due to reports")
            return
        
        info[guildId][channelId][referencedMessage]["reports"].append(message.author.id)
        debug.log(f"[green1][REPORT][green1] [dark_violet]{message.author.id} reported {referencedMessage}")
        
        with open("./info.json", "w") as infoFile:
            json.dump(info, infoFile, indent=4)

    async def imageReactions(self, message):
        info = json.loads(open("./info.json").read())
        guild = str(message.guild.id)
        channel = str(message.channel.id)

        if guild not in info:
            return
        if channel not in info[guild]:
            return

        for attachment in message.attachments:
            if "image" in attachment.content_type:
                attachmentUrl = attachment.url
                break
            if "video" in attachment.content_type:
                attachmentUrl = attachment.url
                break
        else:
            return
                
        info[guild][channel].update({message.id:{"url":attachmentUrl, "score":0, "reports": []}})
        debug.log(f"[green1][ADDED][/green1] [dark_violet]{message.id} with attachment [blue]{attachmentUrl}[/blue][/dark_violet]")

        with open("./info.json", "w") as infoFile:
            json.dump(info, infoFile, indent=4)

        await message.add_reaction("🔼")
        await message.add_reaction("🔽")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.attachments:
            await self.imageReactions(message)
        if message.reference and message.content == "report":
            await self.reportMessage(message)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        info = json.loads(open("./info.json").read())
        guild = str(payload.guild_id)
        channel = str(payload.channel_id)
        message = str(payload.message_id)

        if guild not in info:
            return
        if channel not in info[guild]:
            return

        try:            
            url = info[guild][channel][message]['url']
        except KeyError:
            return

        del info[guild][channel][message]

        with open("info.json", "w") as infoFile:
            json.dump(info, infoFile, indent=4)
        
        debug.log(f"[green1][REMOVED][/green1] [dark_violet]{message} with attachment [blue]{url}[/blue]")

def setup(bot):
    bot.add_cog(reactions(bot))