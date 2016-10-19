import discord
from discord.ext import commands
import inspect

def owner_only():
    """Decorator to check if user is owner."""
    def owner_check(context):
        return context.message.author.id == '106971793868197888'
    return commands.check(owner_check)

class Admin:
    """
    Special debug commands so I can figure out what's going on, because I still
    haven't implemented a proper logging system.
    """
    def __init__(self, bot):
        self.chiaki = bot

    @commands.command(pass_context = True, hidden = True)
    @owner_only()
    async def debug(self, context, *, command):
        """Simple command for executing code."""
        result = eval(command)
        if inspect.isawaitable(result):
            result = await result
        await self.chiaki.say(result)

    @commands.command(hidden = True)
    @owner_only()
    async def logout(self):
        """Exits the bot."""
        await self.chiaki.logout()

def setup(bot):
    bot.add_cog(Admin(bot))
