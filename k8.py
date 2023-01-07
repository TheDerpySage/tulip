import discord
from discord.ext import commands
import random

def mention(user : discord.Member):
    return "<@" + str(user.id) + ">"

class K8Cog(commands.Cog):
    '''K8-Bots old functions.
    Written by LadyTitanium.'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, user : discord.Member = None):
        """Get or Give a hug."""
        if user is None:
            user = ctx.message.author
        random.seed()
        intensity = random.randint(1,10)
        if intensity <= 0:
            msg = "(っ˘̩╭╮˘̩)っ" + mention(user)
        elif intensity <= 3:
            msg = "(っ´▽｀)っ" + mention(user)
        elif intensity <= 6:
            msg = "╰(*´︶`*)╯" + mention(user)
        elif intensity <= 9:
            msg = "(つ≧▽≦)つ" + mention(user)
        elif intensity >= 10:
            msg = "(づ￣ ³￣)づ" + mention(user) + " ⊂(´・ω・｀⊂)"
        await ctx.send(msg)

    @commands.command(name="love", aliases=['I love you'])
    async def love(self, ctx, user : discord.Member = None):
        """Get or Give some love"""
        if user is None:
            user = ctx.message.author
            await ctx.send("I love you too, " + mention(user) + "! <3")
        else : await ctx.send("I love you, " + mention(user) + "! <3")

    @commands.command()
    async def compliment(self, ctx, user : discord.Member = None):
        """Get or give a compliment."""
        if user is None:
            user = ctx.message.author
        random.seed()
        x = random.randint(1,11)
        if x == 1:
            msg = "You’re amazing, " + mention(user) + "!"
        elif x == 2:
            msg = mention(user) + " I think you’re the best!"
        elif x == 3:
            msg = mention(user) + " You’re lovely!"
        elif x == 4:
            msg = mention(user) + " You make me happy!"
        elif x == 5:
            msg = "You’re spectacular, " + mention(user) + "!"
        elif x == 6:
            msg = mention(user) + " You’re a star!"
        elif x == 7:
            msg = mention(user) + " You’re wonderful!"
        elif x == 8:
            msg = mention(user) + " You’re lovely!"
        elif x == 9:
            msg = mention(user) + " You’re adorable!"
        elif x == 10:
            msg = mention(user) + " You make people smile!"
        elif x >= 11:
            msg = mention(user) + " You are loved!"
        await ctx.send(msg)

    @commands.command()
    async def comfort(self, ctx):
        """Offers words."""
        random.seed()
        x = random.randint(1,12)
        if x == 1:
            msg = "I believe in you!"
        elif x == 2:
            msg = "Stay determined!"
        elif x == 3:
            msg = "It’ll be okay."
        elif x == 4:
            msg = "Everything will be okay."
        elif x == 5:
            msg = "You can make it through this."
        elif x == 6:
            msg = "You’re not alone."
        elif x == 7:
            msg = "This too shall pass."
        elif x == 8:
            msg = "Stay determined!"
        elif x == 9:
            msg = "I promise you everything will turn out just fine!"
        elif x == 10:
            msg = "Keep your chin up and keep moving forward. You’re not in this alone!"
        elif x == 11:
            msg = "Keep moving forward."
        elif x >= 12:
            msg = "It’ll get better!"
        await ctx.send(msg)

    @commands.command(aliases=['thank you'])
    async def thanks(self, ctx):
        """Show gratitude."""
        await ctx.send("No problem!")

async def setup(bot):
    await bot.add_cog(K8Cog(bot))
