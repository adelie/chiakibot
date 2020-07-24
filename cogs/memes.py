import discord
from discord.ext import commands
import json
import functools, inspect
import random

class Memes(commands.Cog):
    """
    'Memes were a mistake.' - Richard Dawkins

    Handles simple user-defined commands in the form of command -> response.
    """
    def __init__(self, bot):
        self.chiaki = bot
        try:
            with open('cogs/storage/memes.json') as memes:
                self.loaded = json.load(memes)
        except Exception as e:
            self.loaded = {}

    def initialize(self):
        for name, response in self.loaded.items():
            self.add_command(name, response)

    def add_command(self, name, response):
        """Adds a simple custom command to the bot."""
        command = self.chiaki.get_command(name)
        # custom commands are only added if their name doesn't overlap with
        # an existing 'normal' command. spaces also break things.
        if command is None and ' ' not in name:
            command = self.chiaki.command(name = name, hidden = True)(self.customCommand)

    def remove_command(self, name):
        """Removes custom command."""
        # todo: this can actually break if there's a meme that overlaps with a normal
        # (i.e. non-userdefined command). can probably fix this by using the same
        # class logic as before, but leaving that for when i clean up this code.
        if name in self.loaded.keys():
            self.chiaki.remove_command(name)

    @commands.group(invoke_without_command = True)
    async def meme(self, context, *, meme):
        """Display a meme."""
        meme = meme.lower().strip(' "')
        if meme in self.loaded:
            response = self.loaded[meme]
            if isinstance(response, list):
                response = random.choice(response)
            await context.send(response)

    @meme.command()
    async def list(self, context):
        """Lists all memes currently available."""
        if self.loaded:
            memes = [ meme for meme in self.loaded ]
            response = 'I\'ve recorded memes for: {0}.'
            response = response.format(', '.join(memes))
        else:
            response = 'Somehow in my lifetime of studying memes I have recorded none.'
        await context.send(response)

    @commands.command()
    async def random(self, context):
        """Chooses a random meme."""
        if self.loaded:
            choice = random.choice(list(self.loaded.values()))
            if isinstance(choice, list):
                choice = random.choice(choice)
            await context.send(choice)

    @meme.command(name = 'random')
    async def meme_random(self, context):
        """Chooses a random meme."""
        if self.loaded:
            await context.send(random.choice(list(self.loaded.values())))

    @meme.command()
    async def add(self, context, meme, *, reaction):
        """Add a new meme."""
        meme = meme.lower()
        reaction = reaction.strip(' "')
        if meme in self.loaded:
            response = 'I already have an entry under `{0}`. '
            response += 'To overwrite it, please `?meme remove` the meme first.'
            response = response.format(meme)
        else:
            response = self.loaded[meme] = reaction
            self.add_command(meme, reaction)
            self.save_to_file()
        await context.send(response)

    @meme.command()
    async def addrandom(self, context, meme, *reactions):
        """Adds a new meme that pulls a random response from a list."""
        meme = meme.lower()
        reactions = list(reactions)
        if meme in self.loaded:
            response = 'I already have an entry under `{0}`.'
            response += 'To overwrite it, please `?meme remove` the meme first.'
            response = response.format(meme)
        else:
            self.loaded[meme] = reactions
            self.add_command(meme, reactions)
            self.save_to_file()
            response = random.choice(reactions)
        await context.send(response)

    @meme.command()
    async def info(self, context, *, meme):
        """Get information about a meme."""
        meme = meme.lower().strip(' "')
        if meme in self.loaded:
            response = 'This meme has {0} entries in my archives.'
            if isinstance(self.loaded[meme], list):
                response = response.format(len(self.loaded[meme]))
            else:
                response = response.format(1)
        else:
            response = 'I don\'t know what that is?'
        await context.send(response)

    @meme.command()
    async def remove(self, context, *, meme):
        """Remove a meme."""
        meme = meme.lower().strip(' "')
        if meme in self.loaded:
            self.loaded.pop(meme)
            self.remove_command(meme)
            self.save_to_file()
            response = 'I\'ve removed all reference to `{0}` from my archives.'
            response = response.format(meme)
        else:
            response = 'I don\'t seem to have anything under `{0}`?'
            response = response.format(meme)
        await context.send(response)

    @meme.command()
    async def updateadd(self, context, meme, *reactions):
        """Adds a reaction as a part of a random meme."""
        meme = meme.lower()
        if meme in self.loaded:
            for reaction in reactions:
                reaction = reaction.strip(' "')
                current = self.loaded[meme]
                if isinstance(current, list):
                    current.append(reaction)
                else:
                    current = [current, reaction]
                self.loaded[meme] = current
            self.remove_command(meme)
            self.add_command(meme, current)
            response = reaction
            self.save_to_file()
        else:
            response = 'I don\'t seem to have anything under `{0}`?'
            response = response.format(meme)
        await context.send(response)

    @meme.command()
    async def updateremove(self, context, meme, *, reaction):
        """Removes a reaction from a random meme."""
        meme = meme.lower()
        reaction = reaction.strip(' "')
        if meme in self.loaded and isinstance(self.loaded[meme], list) and reaction in self.loaded[meme]:
            current = self.loaded[meme]
            current.remove(reaction)
            self.loaded[meme] = current
            self.remove_command(meme)
            self.add_command(meme, current)
            self.save_to_file()
            response = random.choice(current)
        else:
            response = 'I don\'t seem to have anything like `{0}`?'
            response = response.format(reaction)
        await context.send(response)

    def save_to_file(self):
        """
        Utility function for saving to a JSON file. Calling it every time something is
        updated seems awfully wasteful, but it'll do for now.
        """
        with open('cogs/storage/memes.json', 'w+') as memes:
            json.dump(self.loaded, memes)

    async def customCommand(self, context):
        response = self.loaded[context.invoked_with]
        if isinstance(response, list):
            response = random.choice(response)
        await context.send(response)
    
def setup(bot):
    bot.add_cog(Memes(bot))
