import json
import discord
from discord.ext import commands
from rich.console import Console

debug = Console()

class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        info = json.loads(open("./info.json").read())

        if message.channel.id not in info["channels"]:
            return
        if not message.attachments:
            return

        for attachment in message.attachments:
            if not "image" in attachment.content_type:
                return

            info["images"].update({message.id:{"img":attachment.url, "score":0}})
            debug.log(f"[green1][IMAGE][/green1] [dark_violet]{message.id} with image [blue]{attachment.url}[/blue] added[/dark_violet]")
            
            with open("./info.json", "w") as infoFile:
                infoFile.seek(0)
                json.dump(info, infoFile, indent=4)

        await message.add_reaction("🔼")
        await message.add_reaction("🔽")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        info = json.loads(open("./info.json").read())
        msgId = str(payload.message_id)

        try:
            del info["images"][msgId]
        except KeyError:
            return 

        with open("info.json", "w") as infoFile:
            infoFile.seek(0)
            json.dump(info, infoFile, indent=4)
        debug.log(f"[green1][DELETE][/green1] [dark_violet]{msgId} deleted")


def setup(bot):
    bot.add_cog(reactions(bot))
