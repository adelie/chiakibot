import discord
from discord.ext import commands
import random, re

operators = { '^' : (lambda a, b: a ** b, 4, 'right'), '*' : (lambda a, b: a * b, 3, 'left'),
              '/' : (lambda a, b: 1.0 * a / b, 3, 'left'), '+' : (lambda a, b: a + b, 2, 'left'),
              '-' : (lambda a, b: a - b, 2, 'left') }

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
        extratag = ""
        if chosen == "die":
            extratag = " (But you really shouldn't.)"
        await self.chiaki.say('I choose you, {0}!{1}'.format(chosen, extratag))

    @commands.command()
    async def roll(self, *, dice):
        """Rolls dice."""
        # this is kind of long, and breaks on a few not-so-weird cases, e.g. negatives.
        # oh well, it works i guess!
        dice = dice.replace(' ', '')
        tokens = re.split('(\+|-|\*|/|\^|\(|\))', dice)

        # if it's a simple NdN statement, we'll show what rolled. this repeats some code but welp.
        if len(tokens) == 1:
            final = self.roll_calculator(dice, True)
            if isinstance(final, list):
                await self.chiaki.say('I rolled {0} for a sum of `{1}`.'.format(', '.join([str(x) for x in final]), str(sum(final))))
                return
        else:
            # parse into postfix notation for use, using the shunting-yard algorithm.
            stack = []
            output = []
            for token in tokens:
                if token in operators:
                    if operators[token][2] == 'left':
                        while stack and stack[-1] in operators and operators[token][1] <= operators[stack[-1]][1]:
                            output.append(stack.pop())
                    elif operators[token][2] == 'right':
                        while stack and stack[-1] in operators and operators[token][1] < operators[stack[-1]][1]:
                            output.append(stack.pop())
                    stack.append(token)
                elif token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    if stack and stack[-1] == '(':
                        stack.pop()
                elif token:
                    output.append(token)
            while stack:
                output.append(stack.pop())

            # now that everything's been parsed, solve and give numbers!
            stack = []
            for token in output:
                if token in operators:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(operators[token][0](a, b))
                else:
                    stack.append(self.roll_calculator(token, False))
            final = stack[0]

        await self.chiaki.say('I rolled `{0}` for a sum of `{1}`.'.format(dice, final))

    def roll_calculator(self, dice, return_list):
        """Helper function for calculating rolls"""
        result = 0
        try:
            result = int(dice)
        except ValueError:
            tokens = dice.split('d')
            if len(tokens) == 1 or not tokens[1].isdigit():
                pass
            else:
                rolls, limit = tokens
                if not rolls:
                    rolls = 1
                rolls, limit = int(rolls), int(limit)
                if return_list and rolls < 100:
                    result = [random.randint(1, limit) for roll in range(rolls)]
                else:
                    for roll in range(rolls):
                        result += random.randint(1, limit)
        return result


def setup(bot):
    bot.add_cog(RNG(bot))
