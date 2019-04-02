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
    """
    def __init__(self, bot):
        self.chiaki = bot
        # load relevant information from our handy-dandy json file.
        # stored as { task_id : (author_id, mentions, note, date, channel_id) }
        # TODO: implement schedules
        try:
            with open('cogs/storage/time.json') as time:
                data = json.load(time)
                self.reminders = { int(key) : value for key, value in data['reminders'].items() }
                self.schedules = { int(key) : value for key, value in data['schedules'].items() }
        except Exception as e:
            self.reminders = {}
            self.schedules = {}
        # set up numbering of items.
        # could be done better, but i'm lazy and this lets me cancel/delete tasks.
        self.id = 1 + max(max(self.reminders) if self.reminders else 0,
                          max(self.schedules) if self.schedules else 0)
        self.tasks = {}
        # start the timer for any pre-loaded information.
        loop = self.chiaki.loop
        for key, item in dict(self.reminders).items():
            time = date_to_seconds(item[3])
            if time > 0 and time < 604800:
                task = loop.create_task(self.start_reminder(key, time))
                self.tasks[key] = task
            elif time <= 0:
                self.reminders.pop(key)
        # schedules loop not here because schedules not implemented, lol.

    @commands.command()
    async def day(self):
        """Shows current day of week."""
        now = datetime.now(tz = pytz.timezone('UTC'))
        est_day = now.astimezone(pytz.timezone('US/Eastern')).strftime("%A")
        pst_day = now.astimezone(pytz.timezone('US/Pacific')).strftime("%A")
        if est_day != pst_day:
            response = '¯\_(ツ)_/¯'
        else:
            response = '{0} greetings to all my online friends!'
            response = response.format(pst_day)
        await self.chiaki.say(response)

    @commands.group(aliases = ['remindme'], pass_context = True, invoke_without_command = True)
    async def remind(self, context, time, *, note):
        """Sets a reminder for you."""
        time = timeleft_to_seconds(time)
        note = note.strip(' "')
        if time:
            date = datetime.utcnow() + timedelta(0, time)
            author = context.message.author
            # i have no idea if this'll cause race conditions, but i don't expect that much use.
            key = self.id = self.id + 1
            self.reminders[key] = (author.id, author.mention, note, date.strftime('%c'),
                                   context.message.channel.id)
            self.tasks[key] = self.chiaki.loop.create_task(self.start_reminder(key, time))
            await self.chiaki.say('Okay, I\'ll remind you in `{0}` seconds!'.format(time))
            self.save_to_file()

    @remind.command(pass_context = True)
    async def list(self, context):
        author = context.message.author
        # this was originally a list comprehension, but i've been informed people would
        # rather murder me than read that.
        # i like the list comprehension better honestly...
        reminders = []
        reminder_format = '{0} : {1} (in {2})'
        for key, item in self.reminders.items():
            if item[0] == author.id:
                time_format = seconds_to_timeleft(date_to_seconds(item[3]))
                reminders.append(reminder_format.format(key, item[2], time_format))
        if reminders:
            response = '\n'.join(reminders)
        else:
            response = 'I don\'t have anything to remind you about.'
        await self.chiaki.say(response)

    @remind.command(pass_context = True)
    async def remove(self, context, reminderId : int):
        if reminderId in self.reminders and self.reminders[reminderId][0] == context.message.author.id:
            self.reminders.pop(reminderId)
            task = self.tasks.pop(reminderId)
            task.cancel()
            await self.chiaki.say('Successfully removed reminder `{0}`.'.format(reminderId))
            self.save_to_file()

    async def start_reminder(self, key, time):
        """
        Starts a timer for the specified amount of time.
        """
        await asyncio.sleep(time)
        # task should be removed, but we may as well be safe.
        if key in self.reminders:
            author, mention, note, date, channel_id = self.reminders.pop(key)
            self.tasks.pop(key)
            response = '{0}, you left a note for yourself: {1}'
            response = response.format(mention, note)
            channel = self.chiaki.get_channel(channel_id)
            await self.chiaki.send_message(channel, response)

    def save_to_file(self):
        """Utility function for saving to a JSON file."""
        with open('cogs/storage/time.json', 'w+') as time:
            json.dump({ 'schedules' : self.schedules, 'reminders' : self.reminders }, time)

### need this for loading extensions to work.
def setup(bot):
    bot.add_cog(Time(bot))

### utility functions for converting time.
def timeleft_to_seconds(data):
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

def date_to_seconds(data):
    """Utility function for converting a date string representation into seconds remaining."""
    date = datetime.strptime(data, '%c')
    now = datetime.utcnow()
    return int((date - now).total_seconds())

def seconds_to_timeleft(seconds):
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
