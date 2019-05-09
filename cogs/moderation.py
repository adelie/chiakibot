import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """
    Commands for channel and role moderation.
    There isn't much here because I'm designed for a private server.
    """
    def __init__(self, bot):
        self.chiaki = bot

    @commands.command(pass_context = True)
    async def topic(self, context, *, text):
        """Changes the topic of the current channel to something else."""
        text = text.strip(' "')
        await self.chiaki.edit_channel(context.message.channel, topic = text)

    @commands.group(pass_context = True, invoke_without_command = True)
    async def color(self, context, *, role):
        role = self.get_role(context, role)
        if not role:
            await self.chiaki.say("There's no role by this name!")
        else:
            await self.chiaki.say("That role is colored {0}.".format(role.color))

    @color.command(pass_context = True)
    async def set(self, context, *, command):
        # check validity of these arguments first.
        role = self.get_role(context, ' '.join(command.split(" ")[:-1]))
        colorCode = command.split(' ')[-1]
        converter = commands.ColourConverter(context, colorCode)
        color = None
        try:
            color = converter.convert()
        except commands.errors.BadArgument:
            pass
        if not role:
            await self.chiaki.say("There's no role by this name!")
            return
        if not color:
            await self.chiaki.say("That's not a valid color!")
            return
        # check to see if legal for user to modify color
        if role not in context.message.author.roles:
            await self.chiaki.say("You don't belong to that role!")
            return
        try:
            await self.chiaki.edit_role(context.message.server, role, color = color)
        except discord.errors.Forbidden:
            await self.chiaki.say("Whoops! I don't have permissions to do that.")
            return
        await self.chiaki.say("Okay, changed your role color!")

    def get_role(self, context, role):
        # start with default converter
        converter = commands.RoleConverter(context, role)
        found = None
        try:
            found = converter.convert()
        except commands.errors.BadArgument:
            pass
        if not found:
            role = role.strip('"').lower()
            def pred(m):
                return (m.name and m.name.lower() == role)
            found = discord.utils.find(pred, context.message.server.roles)
        return found

def setup(bot):
    bot.add_cog(Moderation(bot))
