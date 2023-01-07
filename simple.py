import discord
from discord.ext import commands
import random

class SimpleCog(commands.Cog):
    '''The base stuff'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hi', 'howdy'])
    async def hello(self, ctx):
        """Greet the bot."""
        await ctx.send('Hello.')

    @commands.command()
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices."""
        random.seed()
        if (len(choices) < 2):
            await ctx.send("?")
        else: await ctx.send(random.choice(choices))

    @commands.command(aliases=['is', 'are', 'am', 'does', 'will', 'can', 'do', 'could', 'did', 'should', 'would'])
    async def ask(self, ctx, *, message: str = None ):
        """Ask a Yes or No Question."""
        if message != None:
            random.seed()
            intensity = random.randint(0,10)
            if intensity == 0:
                await ctx.send("Absolutely not.")
            elif intensity < 5:
                await ctx.send("No.")
            elif intensity == 5:
                await ctx.send("Maybe.")
            elif intensity < 10:
                await ctx.send("Yes.")
            elif intensity == 10:
                await ctx.send("Definitely.")
            else: await ctx.send("Go fuck yourself.")
        else: await ctx.send("?")

    @commands.command()
    async def roll(self, ctx, *, message: str = None):
        """Shoot dice. Acceptable format is NdX. Where N is number of dice and X is how many sides."""
        if message != None:
            if message.index('d') >= 0:
                nums = message.split('d')
                try:
                    dice = int(nums[0])
                    sides = int(nums[1])
                except:
                    await ctx.send("?")
                else: 
                    if dice and sides > 0:
                        response = ""
                        for x in range(dice):
                            random.seed()
                            response += "%s, " % random.randint(1, sides)
                        await ctx.send(response[:-2])
        else: await ctx.send("?")

    @commands.command(name="pat", aliases=["head pat", "Pat"])
    async def head_pat(self, ctx, *, message: str = None ):
        ouo = self.bot.get_emoji(643879976998797312)
        await ctx.send(str(ouo))

async def setup(bot):
    await bot.add_cog(SimpleCog(bot))
