import discord
from discord.ext import commands

class Moderation:
    """
    Commands for channel and role moderation.
    There isn't much here because I'm designed for a private server.
    """
    def __init__(self, bot):
        self.chiaki = bot

    @commands.command(pass_context = True)
    async def topic(self, context, *, text):
        """Changes the topic of the current channel to something else."""
        await self.chiaki.edit_channel(context.message.channel, topic = text)

def setup(bot):
    bot.add_cog(Moderation(bot))
