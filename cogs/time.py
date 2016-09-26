import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import pytz
import json
import re

class Time:
    """
    Commands dealing with the passage of time.
    At the moment reminders don't save through reboot.
    They were supposed to, but I'm bad at multithreading.
    """
    def __init__(self, bot):
        self.chiaki = bot
        self.reminders = {}

    @commands.command()
    async def day(self):
        """Shows current day of week."""
        now = datetime.now(tz = pytz.timezone('UTC'))
        est = now.astimezone(pytz.timezone('US/Eastern')).strftime("%A")
        pst = now.astimezone(pytz.timezone('US/Pacific')).strftime("%A")
        if est != pst:
            await self.chiaki.say('¯\_(ツ)_/¯')
        else:
            await self.chiaki.say('{0} greetings to all my online friends!'.format(pst))

    @commands.group(aliases = ['remindme'], pass_context = True, invoke_without_command = True)
    async def remind(self, context, time, *, note):
        """Sets a reminder for you."""
        time = self.timeleft_to_seconds(time)
        if time:
            future = datetime.now(tz = pytz.timezone('UTC')) + timedelta(0, time)
            author = context.message.author
            # i have no idea if this'll cause race conditions, but i don't expect that much use.
            key = max(self.reminders.keys()) + 1 if self.reminders else 1
            self.reminders[key] = (author.id, note, future.strftime('%c'))
            await self.chiaki.say('Okay, I\'ll remind you in `{0}` seconds!'.format(time))
            await self.start_reminder(key, time, author.mention, note)

    @remind.command(pass_context = True)
    async def list(self, context):
        author = context.message.author
        reminders = [ '{0}: {1} (in {2})'.format(key, data[1], self.seconds_to_timeleft(self.seconds(data[2]))) for key, data in self.reminders.items() if data[0] == author.id ]
        if reminders:
            await self.chiaki.say('\n'.join(reminders))
        else:
            await self.chiaki.say('I don\'t have anything to remind you about.')

    @remind.command(pass_context = True)
    async def remove(self, context, reminderId : int):
        if reminderId in self.reminders and self.reminders[reminderId][0] == context.message.author.id:
            self.reminders.pop(reminderId)
            await self.chiaki.say('Successfully removed reminder `{0}`.'.format(reminderId))

    async def start_reminder(self, key, time, mention, note):
        """
        Starts a timer for the specified amount of time.
        """
        await asyncio.sleep(time)
        # this allows removal of reminders after they've started
        # TODO: make this not look like suffering.
        if key in self.reminders:
            self.reminders.pop(key)
            await self.chiaki.say('{0}, you left a note for yourself: {1}'.format(mention, note))

    def timeleft_to_seconds(self, data):
        """Utility function that'll take a string of format NdNhNmNs and return a number of seconds."""
        if data.isdigit():
            return int(data)
        else:
            match = re.match('(?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?', data)
            if match is None:
                return 0
            days = match.group('days') or 0
            hours = match.group('hours') or 0
            minutes = match.group('minutes') or 0
            seconds = match.group('seconds') or 0
            return int(days) * 86400 + int(hours) * 3600 + int(minutes) * 60 + int(seconds)

    def seconds(self, data):
        """Utility function for converting a date string representation into seconds remaining."""
        date = datetime.strptime(data, '%c')
        now = datetime.utcnow()
        return (date - now).seconds

    def seconds_to_timeleft(self, seconds):
        """Utilty function converting seconds to string representation."""
        days, seconds = seconds // 86400, seconds % 86400
        hours, seconds = seconds // 3600, seconds % 3600
        minutes, seconds = seconds // 60, seconds % 60
        timeleft = ''
        if days:
            timeleft += '{0}d'.format(days)
        if hours:
            timeleft += '{0}h'.format(hours)
        if minutes:
            timeleft += '{0}m'.format(minutes)
        if seconds:
            timeleft += '{0}s'.format(seconds)
        return timeleft

    def save_to_file(self):
        """Utility function for saving to a JSON file."""
        with open('cogs/storage/time.json', 'w+') as nicknames:
            json.dump({ 'schedules' : self.schedules, 'reminders' : self.reminders }, nicknames)

def setup(bot):
    bot.add_cog(Time(bot))
