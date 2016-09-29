import discord
from discord.ext import commands

class Misc:
    """I'm not very good at categorizing things."""
    def __init__(self, bot):
        self.chiaki = bot

    @commands.command()
    async def say(self, *, repeat):
        """A generic repeat command."""
        await self.chiaki.say(repeat)

    @commands.command()
    async def handhold(self):
        """Sex is lewd because it can lead to handholding."""
        await self.chiaki.say('That\'s l-lewd!')

    @commands.command(pass_context = True)
    async def nerd(self, context, *, user):
        """Determines if user is a nerd."""
        # this is legit just an in-joke function.
        user = self.chiaki.get_cog('Nicknames').get_member(context, user)
        if not user:
            response = 'I don\'t know who that is?'
        elif user.id == '106971793868197888':
            response = '{0} is a cute anime girl.'.format(user.display_name)
        elif user.bot:
            response = '..........'
        else:
            response = '{0} is most definitely a nerd.'.format(user.display_name)
        await self.chiaki.say(response)

def setup(bot):
    bot.add_cog(Misc(bot))
