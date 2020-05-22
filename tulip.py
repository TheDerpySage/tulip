import discord
from discord.ext import commands
import discord.abc
import sys, traceback
from datetime import datetime
import bot_config

def get_prefix(bot, msg):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = [bot.user.name[0:1].lower()+'$', bot.user.name+', ', "Ladies, ", "Tulip, "]
    # Check to see if we are outside of a guild. e.g DM's etc.
    if msg.channel is None:
        return ''
    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, msg)

desc = '''Written and Developed by theDerpySage'''

startup_extensions = ['simple', 'k8', 'admin', 'music']
bot = commands.Bot(command_prefix=get_prefix,description=desc)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='Use '+bot.user.name[0:1].lower()+'$help'))
    if __name__ == '__main__':
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except:
                print('Failed to load extension ' + extension, file=sys.stderr)
                traceback.print_exc()
    print('Successfully logged in and booted...!')

@bot.event
async def on_message(message):
    #Log Channel for her DMs
    log_channel = bot.get_channel(585857730150137876)
    #Checks if its a DM
    if isinstance(message.channel, discord.abc.PrivateChannel):
        #Makes sure it's not her talking, may be a good idea to delete just to make sure DMs are actually sending...
        if message.author.id != 555277319430733835: 
            #Sends message to the logs channel with the Name, ID, and message from the DM
            await log_channel.send(datetime.now().strftime("%b %d %Y, %I:%M %p") + " : " + message.author.name + "/" + str(message.author.id) + " : " + message.content)
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("?")
    raise error

bot.run(bot_config.token, reconnect=True)
