import discord
from discord.ext import commands
import json
import traceback, sys
import logging

chiaki = commands.Bot(command_prefix = '?' ,
                      description = 'There are a lot of things I still don\'t understand.')
extensions = [ 'cogs.admin', 'cogs.memes', 'cogs.misc', 'cogs.moderation' , 'cogs.rng',
               'cogs.time', 'cogs.nicknames' ]

## something keeps killing her so i'll just add logging..
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='chiaki.log', encoding='utf-8', mode='w')
log.addHandler(handler)

@chiaki.event
async def on_ready():
    print('Logged in as {0} ({1}).'.format(chiaki.user.name, chiaki.user.id))

@chiaki.event
async def on_message(message):
    if message.author.bot:
        return
    # kill me for being guilt-tripped into writing this
    if message.content[0] != '?' and 'ayy' in message.content.split():
        await chiaki.send_message(message.channel, 'lmao')
    await chiaki.process_commands(message)

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
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        log.warning(traceback.format_exception_only(type(error), error)[0])

@chiaki.event
async def on_command(command, context):
    message = context.message
    log.info('{0.timestamp}: {0.author.name}: {0.content}'.format(message))

def load_config():
    with open('config.json') as config:
        return json.load(config)

def run_chiaki():
    config = load_config()
    for extension in extensions:
        try:
            chiaki.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {0}: {1}'.format(extension, e))
    chiaki.run(config['token'])

run_chiaki()
