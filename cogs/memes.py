import discord
from discord.ext import commands
import json
import functools, inspect
import random

class Memes:
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
            command = self.chiaki.command(name = name, cls = CustomCommand,
                           pass_context = True, hidden = True)(custom_callback)
            command.response = response

    def remove_command(self, name):
        """Removes custom command."""
        command = self.chiaki.get_command(name)
        if isinstance(command, CustomCommand):
            self.chiaki.remove_command(name)

    @commands.group(invoke_without_command = True)
    async def meme(self, *, meme):
        """Display a meme."""
        meme = meme.lower().strip(' "')
        if meme in self.loaded:
            response = self.loaded[meme]
            if isinstance(response, list):
                response = random.choice(response)
            await self.chiaki.say(response)

    @meme.command()
    async def list(self):
        """Lists all memes currently available."""
        if self.loaded:
            memes = [ meme for meme in self.loaded ]
            response = 'I\'ve recorded memes for: {0}.'
            response = response.format(', '.join(memes))
        else:
            response = 'Somehow in my lifetime of studying memes I have recorded none.'
        await self.chiaki.say(response)

    @commands.command()
    async def random(self):
        """Chooses a random meme."""
        if self.loaded:
            choice = random.choice(list(self.loaded.values()))
            if isinstance(choice, list):
                choice = random.choice(choice)
            await self.chiaki.say(choice)

    @meme.command(name = 'random')
    async def meme_random(self):
        """Chooses a random meme."""
        if self.loaded:
            await self.chiaki.say(random.choice(list(self.loaded.values())))

    @meme.command()
    async def add(self, meme, *, reaction):
        """Add a new meme."""
        meme = meme.lower()
        reaction = reaction.strip(' "')
        if meme in self.loaded:
            response = 'I already have an entry under `{0}`. To overwrite it, use `?meme update`.'
            response = response.format(meme)
        else:
            response = self.loaded[meme] = reaction
            self.add_command(meme, reaction)
            self.save_to_file()
        await self.chiaki.say(response)

    @meme.command()
    async def addrandom(self, meme, *reactions):
        """Adds a new meme that pulls a random response from a list."""
        meme = meme.lower()
        reactions = list(reactions)
        if meme in self.loaded:
            response = 'I already have an entry under `{0}`. To overwrite it, use `?meme update`.'
            response = response.format(meme)
        else:
            self.loaded[meme] = reactions
            self.add_command(meme, reactions)
            self.save_to_file()
            response = random.choice(reactions)
        await self.chiaki.say(response)

    @meme.command()
    async def remove(self, *, meme):
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
        await self.chiaki.say(response)

    """
    @meme.command()
    async def update(self, meme, *, reaction):
        meme = meme.lower()
        reaction = reaction.strip(' "')
        if meme in self.loaded:
            response = self.loaded[meme] = reaction
            # removes and reimplements command.
            # unfortunately updating the command causes errors i don't understand.
            self.remove_command(meme)
            self.add_command(meme, reaction)
            self.save_to_file()
        else:
            response = 'I don\'t seem to have anything under `{0}`?'
            response = response.format(meme)
        await self.chiaki.say(response)
    """

    @meme.command()
    async def updateadd(self, meme, *reactions):
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
        await self.chiaki.say(response)

    @meme.command()
    async def updateremove(self, meme, *, reaction):
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
        await self.chiaki.say(response)

    def save_to_file(self):
        """
        Utility function for saving to a JSON file. Calling it every time something is
        updated seems awfully wasteful, but it'll do for now.
        """
        with open('cogs/storage/memes.json', 'w+') as memes:
            json.dump(self.loaded, memes)

class CustomCommand(commands.Command):
    """
    Implementation for custom commands.
    This allows entries in the ?memes list to be called as their own commands,
    if a command by that name doesn't exist already.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = ''

    async def invoke(self, context):
        server = context.message.server
        if server is not None:
            self.callback = functools.partial(custom_callback, self.response)
            self.params = inspect.signature(self.callback).parameters
            await super().invoke(context)

async def custom_callback(response, context):
    if isinstance(response, list):
        response = random.choice(response)
    await context.bot.send_message(context.message.channel, response)

def setup(bot):
    bot.add_cog(Memes(bot))
