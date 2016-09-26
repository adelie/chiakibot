## Chiakibot

Chiaki is a rudimentary Discord bot built on [discord.py](https://github.com/Rapptz/discord.py) and based heavily on example code snippets from around the web. In other words, it's the lovechild of sleep deprivation, incoherent Google searches, and what little Python I actually remember.

Much of the code committed is a 'draft' of possible functions and is planned to be cleaned up in the future.

### Use

I'm not sure who in their right mind would want to run an instance of this. This is only being released on the off chance someone who knows even less Python than I do is looking for examples and thinks the benefits of more open-source code outweighs the struggle of puzzling through nonsensical docstrings and illegible comments.

You'll need two things not in this repository to run an instance of Chiakibot. First, a config.json file in the main directory:

```
{
  "token" : "whatever your discord application token is"
}
```

and second, a folder named storage in the cogs directory. JSON files for that folder will be generated automatically, but if the folder doesn't exist to begin with, things die.
