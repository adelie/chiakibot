import discord
from discord.ext import commands
import json
import traceback, sys
import logging
import re
import time

## bot configuration
chiaki = commands.Bot(command_prefix = '?' ,
                      description = 'There are a lot of things I still don\'t understand.')
extensions = [ 'cogs.admin', 'cogs.memes', 'cogs.misc', 'cogs.moderation' , 'cogs.rng',
               'cogs.time', 'cogs.nicknames' ]

## add some logging since she randomly dies a lot
log = logging.getLogger('chiaki')
log.setLevel(logging.INFO)
filename = 'chiaki-{0}.log'.format(time.strftime('%m%d%y', time.localtime()))
handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='w')
log.addHandler(handler)

@chiaki.event
async def on_ready():
    print('Logged in as {0} ({1}). Let\'s go!'.format(chiaki.user.name, chiaki.user.id))

ayy = re.compile('\\bayy+\\b')
@chiaki.event
async def on_message(message):
    # kill me please i was forced to write this
    if message.content and ayy.search(message.content):
        await chiaki.send_message(message.channel, 'lmao')
    if message.author.bot:
        return
    await chiaki.process_commands(message)

@chiaki.event
async def on_command(command, context):
    message = context.message
    log.info('{0.timestamp}: {0.author.name}: {0.content}'.format(message))

@chiaki.event
async def on_command_error(error, context):
    if isinstance(error, commands.MissingRequiredArgument):
        # if command is used incorrectly, politely correct with usage signature.
        formatter = commands.HelpFormatter()
        formatter.context = context
        formatter.command = context.command
        usage = 'Usage: `{0}`'.format(formatter.get_command_signature())
        await chiaki.send_message(context.message.channel, usage)
    else:
        log.warning(traceback.format_exception_only(type(error), error)[0])

def load_config():
    with open('config.json') as config:
        return json.load(config)

# let's go and run this bot!
config = load_config()
for extension in extensions:
    try:
        chiaki.load_extension(extension)
    except Exception as e:
        print('Failed to load extension {0}: {1}'.format(extension, e))
chiaki.get_cog('Memes').initialize()
chiaki.run(config['token'])
