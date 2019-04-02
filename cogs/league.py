import discord
from discord.ext import commands
import requests, random

insults = ['Looks like they need to git gud.', 'That\'s almost better than an intermediate bot.',
           '{0} IN 2017 LUL', 'They might\'ve taken the advice to not care about winning or losing too far.',
           'I could do better playing Jayce support one-handed.', 'TSM TSM TSM?']

class League:
    """Commands related to League of Legends."""
    def __init__(self, bot):
        self.chiaki = bot

    @commands.group(invoke_without_command = False)
    async def league(self):
        """Legends of Legends is a good solution for low sodium content."""
        pass

    @league.command()
    async def lookup(self, *, summonername):
        """Looks up some useful information on the given summoner."""
        # this uses quite a few api calls so don't get carried away.
        # first, we have to find their id to get anything useful.
        summonername = summonername.lower().replace(' ', '')
        rate_limit_error = 'Oops! If you submit too many requests, Riot Games will fine CLG or something. Try again later.'
        summoner_by_name = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/{0}?api_key={1}'
        r = requests.get(summoner_by_name.format(summonername, self.riot_key))
        if r.status_code == 429:
            # this is repetitive, but welp.
            await self.chiaki.say(rate_limit_error)
            return
        response = r.json()[summonername.lower()]
        summonerid = response['id']
        summonername = response['name']

        # find their ranking
        league_ranking = 'https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/{0}?api_key={1}'
        r = requests.get(league_ranking.format(summonerid, self.riot_key))
        if r.status_code == 429:
            await self.chiaki.say(rate_limit_error)
            return
        elif r.status_code == 404:
            rank = 'UNRANKED'
        else:
            # this is very rough and doesn't account for a lot of different things. :x
            response = r.json()[str(summonerid)][0]
            rank = '{0} {1} with {2} LP'.format(response['tier'], response['entries'][0]['division'],
                                                response['entries'][0]['leaguePoints'])

        await self.chiaki.say('{0} is currently {1}. {2}'.format(summonername, rank, random.choice(insults).format(rank)))

    @league.command(aliases = ['ban'])
    async def bans(self):
        """Returns most completely banned champions."""
        most_banned = 'http://api.champion.gg/stats/champs/mostBanned?api_key={0}&page=1&limit=10'
        r = requests.get(most_banned.format(self.chgg_key))
        champions = []
        for champion in r.json()["data"]:
            data = '{0} ({1}%)'.format(champion["name"], champion["general"]["banRate"])
            if data not in champions:
                champions.append(data)
        await self.chiaki.say('The current most banned champions are {0}.'.format(', '.join(champions)))





def setup(bot):
    bot.add_cog(League(bot))
