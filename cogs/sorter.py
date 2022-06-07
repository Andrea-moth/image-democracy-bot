from discord.ext import commands

#will added later

class sorting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
def setup(bot):
    bot.add_cog(sorting(bot))
