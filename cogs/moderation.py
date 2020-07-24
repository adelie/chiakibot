import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """
    Commands for channel and role moderation.
    There isn't much here because I'm designed for a private server.
    """
    def __init__(self, bot):
        self.chiaki = bot

    @commands.command()
    async def topic(self, context, *, text):
        """Changes the topic of the current channel to something else."""
        text = text.strip(' "')
        await context.message.channel.edit(topic = text)

    @commands.group(pass_context = True, invoke_without_command = True)
    async def color(self, context, *, role):
        role = await self.get_role(context, role)
        if not role:
            await context.send("There's no role by this name!")
        else:
            await context.send("That role is colored {0}.".format(role.color))

    @color.command()
    async def set(self, context, *, command):
        # check validity of these arguments first.
        role = await self.get_role(context, ' '.join(command.split(" ")[:-1]))
        colorCode = command.split(' ')[-1]
        color = None
        try:
            color = await commands.ColourConverter().convert(context, colorCode)
        except commands.errors.BadArgument:
            pass
        if not role:
            await context.send("There's no role by this name!")
            return
        if not color:
            await context.send("That's not a valid color!")
            return
        # check to see if legal for user to modify color
        if role not in context.message.author.roles:
            await context.send("You don't belong to that role!")
            return
        try:
            await role.edit(color = color)
        except discord.errors.Forbidden:
            await context.send("Whoops! I don't have permissions to do that.")
            return
        await context.send("Okay, changed your role color!")

    async def get_role(self, context, role):
        # start with default converter
        found = None
        try:
            found = await commands.RoleConverter().convert(context, role)
        except commands.errors.BadArgument:
            pass
        if not found:
            role = role.strip('"').lower()
            def pred(m):
                return (m.name and m.name.lower() == role)
            found = discord.utils.find(pred, context.message.guild.roles)
        return found

def setup(bot):
    bot.add_cog(Moderation(bot))
