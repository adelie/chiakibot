## Commands

I'm adding text documentation because there's a lot of stuff the built-in ?help command doesn't cover. Of course, this is mostly my fault for not writing good comments.

### General Notes

If your argument contains spaces, put it in quotation marks unless it's the last argument. For example: `?nickname add "Adelie Penguin" absolutely adorable`

Commands are case sensitive, but arguments usually are not. For example: `?nerd adelie` will work the same as `?nerd Adelie`, but `?Nerd adelie` won't work at all.

If the command references a user, you can either use the @mention, their name, their display name, or a nickname.

### Commands

#### Memes

`?meme <name>` will bring up the user-defined command with that name. `?<name>` will do the same thing if that doesn't overlap with another command.

`?meme add <name> <response>` adds a user-defined command, where calls to it will bring up the response. Ideally, you'd put image URLs in here or something.

`?meme remove <name>` `?meme update <name> <response>` do exactly what it says on the tin.

`?meme list` brings up a list of every user-defined command.

`?meme addrandom <name> <responses>` adds a meme that pulls one of many possible responses.

#### Moderation

`?topic <topic>` changes the topic of the channel. Chiaki needs permissions, you don't.

#### Nicknames

`?nicknames <user>` lists all the nicknames a user has. You can use these nicknames in other commands that require users, although at the moment only the nickname function ... actually uses these.

`?nicknames add <user> <nickname>` `nicknames remove <user> <nickname>` are self-explanatory.

#### RNG

`?choose <option> <option> ...` will return one of the given options.

`?coinflip` rolls a d2.

`?roll <AdN>` will roll A dice with N sides.

#### Time

`?day` tells you what day it is.

`?remind <time> <note>` will mention you with the given note after time has passed. Give times in the format `NdNhNmNs` (they're optional).

`?remind list` lists all the reminders you've set up for yourself, with helpful reference IDs.

`?remind remove <id>` will remove the reminder with the ID given.
