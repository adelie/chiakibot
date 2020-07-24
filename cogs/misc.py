import discord
from discord.ext import commands

class Misc(commands.Cog):
    """I'm not very good at categorizing things."""
    def __init__(self, bot):
        self.chiaki = bot

    @commands.command()
    async def say(self, context, *, repeat):
        """A generic repeat command."""
        await context.send(repeat)

    @commands.command()
    async def handhold(self, context):
        """Sex is lewd because it can lead to handholding."""
        await context.send('That\'s l-lewd!')

    @commands.command()
    async def nerd(self, context, *, user):
        """Determines if user is a nerd."""
        user = await self.chiaki.get_cog('Nicknames').get_member(context, user)
        if not user:
            response = 'I don\'t know who that is?'
        # that's me!
        elif user.id == 106971793868197888:
            response = '{0} is a cute anime girl.'.format(user.display_name)
        elif user.bot:
            response = '..........'
        else:
            response = '{0} is most definitely a nerd.'.format(user.display_name)
        await context.send(response)

    @commands.command()
    async def icon(self, context, *, user):
        """Links to a larger version of the user's icon."""
        user = await self.chiaki.get_cog('Nicknames').get_member(context, user)
        if not user:
            response = 'I don\'t know who that is?'
        else:
            response = user.avatar_url
        await context.send(response)

def setup(bot):
    bot.add_cog(Misc(bot))
