import discord
from discord.ext import commands
import json
import traceback, sys


chiaki = commands.Bot(command_prefix = '?' ,
                      description = 'There are a lot of things I still don\'t understand.')
extensions = [ 'cogs.memes', 'cogs.misc', 'cogs.moderation' , 'cogs.rng', 'cogs.time', 'cogs.nicknames' ]

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
