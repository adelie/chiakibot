import discord
from discord.ext import commands
import json
import traceback, sys
import logging
import re
import time

## BASIC BOT CONFIGURATION ----------------------------------------------------
chiaki = commands.Bot(command_prefix = '?' ,
                      description = 'There are a lot of things I still don\'t understand.')
extensions = [
    'cogs.admin',
    'cogs.memes',
    'cogs.misc',
    'cogs.moderation',
    'cogs.nicknames',
    'cogs.rng',
    'cogs.time',
]


## LOGGING HANDLER ------------------------------------------------------------
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')

# logs to file scoped by month. lazy way to fake having monthly log rotation.
filename = 'logs/chiaki-{0}.log'.format(time.strftime('%m%y', time.localtime()))
handler = logging.FileHandler(filename=filename, encoding='utf-8', mode='a+')
handler.setFormatter(formatter)
log.addHandler(handler)

# logs to console
console = logging.StreamHandler()
console.setFormatter(formatter)
log.addHandler(console)


## ACTUAL BOT CODE ------------------------------------------------------------
@chiaki.event
async def on_ready():
    log.info('Logged in as {0} ({1}). Let\'s go!'.format(chiaki.user.name, chiaki.user.id))

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
async def on_command(context):
    log.info('{0.author.name}: {0.content}'.format(context.message))

@chiaki.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # if command is used incorrectly, politely correct with usage signature.
        usage = 'Usage: `{0}`'.format(getCommandSignature(context.command))
        await context.send(usage)
    else:
        log.error('{0.author.name}: {0.content}'.format(context.message))
        log.error(''.join(traceback.format_exception(type(error), error, error.__traceback__)))

# submethod to get command signature
# copied from implementation of HelpCommand. 
def getCommandSignature(command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = '[%s|%s]' % (command.name, aliases)
            if parent:
                fmt = parent + ' ' + fmt
            alias = fmt
        else:
            alias = command.name if not parent else parent + ' ' + command.name

        return '%s%s %s' % ('?', alias, command.signature)

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
# run some extra on-initialize content here.
chiaki.get_cog('Memes').initialize()
# all done, let's go!
chiaki.run(config['token'])
