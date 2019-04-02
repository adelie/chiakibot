import discord
from discord.ext import commands
import json

class Nicknames:
    """
    Deals with identifying members and other things.
    I've been informed that JSON is reasonable data storage. I pray that is correct.
    """
    def __init__(self, bot):
        self.chiaki = bot
        try:
            with open('cogs/storage/nicknames.json') as nicknames:
                self.loaded = json.load(nicknames)
        except Exception as e:
            self.loaded = {}

    def get_member(self, context, user):
        """Returns the discord.Member instance of a user, given some string."""
        # this might break things if someone's name has "'s in it but WHY
        user = user.strip('"')
        converter = commands.MemberConverter(context, user)
        member = None
        # we first start by applying the built-in converter, which'll catch mentions and direct names.
        try:
            member = converter.convert()
        except commands.BadArgument:
            pass
        # didn't work? let's try doing the same thing, but not case sensitive
        user = user.lower()
        def pred(m):
            return (m.nick and m.nick.lower() == user) or (m.name and m.name.lower() == user)
        if not member:
            member = discord.utils.find(pred, context.message.server.members)
        # did we still not find it? let's check nicknames.
        if not member:
            if user in self.loaded:
                member = context.message.server.get_member(self.loaded[user])
        return member

    @commands.group(aliases = ['nickname'], pass_context = True, invoke_without_command = True)
    async def nicknames(self, context, *, member):
        """Display nicknames for a given member."""
        if member in self.loaded:
            actual_user = context.message.server.get_member(self.loaded[member])
            await self.chiaki.say('{0} is the nickname of `{1}`.'.format(member, actual_user.display_name))
        else:
            member = self.get_member(context, member)
            if member:
                nicknames = [ '`{0}`'.format(nickname) for nickname, userId in self.loaded.items() if userId == member.id ]
                if nicknames:
                    await self.chiaki.say('{0} is also known as {1}.'.format(member.display_name, ', '.join(nicknames)))
                else:
                    await self.chiaki.say('I don\'t have any nicknames stored for {0}.'.format(member.display_name))

    @nicknames.command(pass_context = True)
    async def add(self, context, member, *, nickname):
        """Add a new nickname."""
        member = self.get_member(context, member)
        nickname = nickname.lower()
        if nickname in self.loaded:
            named_user = context.message.server.get_member(self.loaded[nickname])
            await self.chiaki.say('`{0}` is already the nickname of {1}'.format(nickname, named_user.display_name))
        elif member:
            self.loaded[nickname] = member.id
            self.save_to_file()
            await self.chiaki.say('From this day forward, {0} shall also be known as `{1}`!'.format(member.display_name, nickname))
        else:
            await self.chiaki.say('There doesn\'t seem to be a user named that?')

    @nicknames.command(pass_context = True)
    async def remove(self, context, member, *, nickname):
        """Remove a nickname from a user."""
        member = self.get_member(context, member)
        nickname = nickname.lower()
        if not member:
            await self.chiaki.say('There doesn\'t seem to be a user named that?')
        elif nickname not in self.loaded or self.loaded[nickname] != member.id:
            await self.chiaki.say('{0} doesn\'t seem to go by the nickname `{1}`'.format(member.display_name, nickname))
        else:
            self.loaded.pop(nickname)
            await self.chiaki.say('{0}, you shall be `{1}` no longer!'.format(member.display_name, nickname))

    def save_to_file(self):
        """Utility function for saving to a JSON file."""
        with open('cogs/storage/nicknames.json', 'w+') as nicknames:
            json.dump(self.loaded, nicknames)

def setup(bot):
    bot.add_cog(Nicknames(bot))
