import discord
from discord.ext import commands
import json
import functools, inspect

class Memes:
    """
    'Memes were a mistake.' - Richard Dawkins

    Handles user-defined commands and images.
    """
    def __init__(self, bot):
        self.chiaki = bot
        try:
            with open('cogs/storage/memes.json') as memes:
                self.loaded = json.load(memes)
        except Exception as e:
            self.loaded = {}
        for name, response in self.loaded.items():
            self.add_command(name, response)

    def add_command(self, name, response):
        """Adds a simple custom command to the bot."""
        command = self.chiaki.get_command(name)
        if command is None:
            command = self.chiaki.command(name = name, cls = CustomCommand,
                                          pass_context = True, hidden = True)(custom_callback)
            command.response = response

    def remove_command(self, name):
        """Removes custom command."""
        command = self.chiaki.get_command(name)
        if isinstance(command, CustomCommand):
            self.chiaki.remove_command(name)

    @commands.command()
    async def memes(self):
        """Lists all memes currently available."""
        if self.loaded:
            memes = [ '`{0}`'.format(meme) for meme in self.loaded ]
            await self.chiaki.say('I\'ve recorded memes for: {0}.'.format(', '.join(memes)))
        else:
            await self.chiaki.say('There\'s nothing in my records!')

    @commands.group(invoke_without_command = True)
    async def meme(self, *, meme):
        """Display a meme."""
        meme = meme.lower()
        if meme in self.loaded:
            await self.chiaki.say(self.loaded[meme])

    @meme.command()
    async def add(self, meme, address):
        """Add a new meme."""
        meme = meme.lower()
        if (meme in ['add', 'remove', 'update'] or meme.startswith('add ') or meme.startswith('remove ')
            or meme.startswith('update ')):
            await self.chiaki.say('I can\'t add anything that starts with `add`, `remove`, or `update`.')
        elif meme in self.loaded:
            await self.chiaki.say('I already have an entry under `{0}`. To overwrite it, use `?meme update`.'.format(meme))
        else:
            self.loaded[meme] = address
            self.add_command(meme, address)
            self.save_to_file()
            await self.chiaki.say(self.loaded[meme])

    @meme.command()
    async def remove(self, *, meme):
        """Remove a meme."""
        meme = meme.lower()
        if meme in self.loaded:
            self.loaded.pop(meme)
            self.remove_command(meme)
            self.save_to_file()
            await self.chiaki.say('I\'ve removed all reference to `{0}` from my archives.'.format(meme))
        else:
            await self.chiaki.say('I don\'t seem to have anything under `{0}`?'.format(meme))

    @meme.command()
    async def update(self, meme, address):
        """Update an existing meme to a new address."""
        meme = meme.lower()
        if meme in self.loaded:
            self.loaded[meme] = address
            self.remove_command(meme)
            self.add_command(meme, address)
            self.save_to_file()
            await self.chiaki.say(address)
        else:
            await self.chiaki.say('I don\'t seem to have anything under `{0}`?'.format(meme))

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
    I honestly have no idea what I'm doing.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = ''

    async def invoke(self, context):
        server = context.message.server
        if server is not None:
            self.callback = functools.partial(self.callback, self.response)
            self.params = inspect.signature(self.callback).parameters
            await super().invoke(context)

async def custom_callback(response, context):
    await context.bot.send_message(context.message.channel, response)

def setup(bot):
    bot.add_cog(Memes(bot))
