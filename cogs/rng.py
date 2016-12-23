import discord
from discord.ext import commands
import random

class RNG:
    """Commands related to random number generation."""
    def __init__(self, bot):
        self.chiaki = bot

    @commands.command()
    async def coinflip(self):
        """Rolls a d2."""
        coin = 'heads' if random.randint(0, 1) else 'tails'
        await self.chiaki.say('I rolled a two-sided dice, and it came up `{0}`.'.format(coin))

    @commands.command()
    async def choose(self, *options):
        """Chooses one of many options."""
        chosen = options[random.randint(0, len(options) - 1)]
        await self.chiaki.say('I choose you, {0}!'.format(chosen))

    @commands.command()
    async def roll(self, *, dice):
        """Rolls dice."""
        # TODO: this is meant to be a proper dice notation parser, but parsing is hard.
        tokens = dice.split('d')
        if len(tokens) == 1 or not tokens[1].isdigit():
            await self.chiaki.say('Oops! I can\'t roll dice that aren\'t in NdN format.')
        else:
            rolls, limit = tokens
            rolls, limit = int(rolls), int(limit)
            if rolls >= 999:
                await self.chiaki.say('Please stop trying to commit bot murder.')
                return
            if not rolls:
                rolls = 1
            roll = [random.randint(1, limit) for roll in range(rolls)]
            await self.chiaki.say('I rolled {0} for a sum of `{1}`.'.format(', '.join([str(x) for x in roll]), str(sum(roll))))

def setup(bot):
    bot.add_cog(RNG(bot))
