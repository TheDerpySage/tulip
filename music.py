import discord
import subprocess
import os
import socket
import asyncio
from datetime import timedelta
from discord.ext import commands, tasks

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_now_playing.start()

    def cog_unload(self):
        self.status_now_playing.cancel()

    @commands.command(aliases=['system', 'server', 'health'])
    async def system_info(self, ctx):
        """Returns information about her Server"""
        host = socket.getfqdn()
        ldavg_tup = os.getloadavg()
        ldavg_string = ""
        for num in ldavg_tup:
            ldavg_string += "%s " % round(num, 2)
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))
        await ctx.send("**System Info**\nHost: " + host + "\nLoad: " + ldavg_string + "\nUptime: " + uptime_string)

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        try:
            if channel is None:
                channel = ctx.author.voice.channel
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)
            await channel.connect()
        except Exception as e:
            await ctx.send("**`ERROR: %s`**" % e)

    @commands.command()
    async def play(self, ctx):
        """Tunes Unicorn Radio"""
        await ctx.send('Clearing the Static, this may take a second...')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("http://127.0.0.1:8000/mpd.ogg"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        ctx.voice_client.source.volume = 0.05
        await ctx.send("Volume set to 5%")

    @commands.command()
    async def now_playing(self, ctx):
        """Shows what's currently playing"""
        try:
            ps = subprocess.Popen(["mpc", "status"], stdout=subprocess.PIPE)
            result = subprocess.run(["head", "-n", "2"], stdin=ps.stdout, stdout=subprocess.PIPE)
            decode = result.stdout.decode('utf-8')
            decode = decode.split("\n")
            if decode[0][0:4] == 'http' : decode = "From Youtube"
            await self.bot.change_presence(activity=discord.Game(name=f'{decode[0]}'))
            await ctx.send("```\n" + decode[0] + "\n" + decode[1] + "```")
        except Exception as e:
            await ctx.send("**`ERROR: %s`**" % e)

    @commands.command()
    async def up_next(self, ctx):
        """Show what's coming up next"""
        ps1 = subprocess.Popen(["mpc", "playlist"], stdout=subprocess.PIPE)
        ps2 = subprocess.Popen(["tail", "-n", "+2"], stdin=ps1.stdout, stdout=subprocess.PIPE)
        result = subprocess.run(["head", "-n", "5"], stdin=ps2.stdout, stdout=subprocess.PIPE)
        decode = result.stdout.decode('utf-8')
        decode = decode.split("\n")
        temp = ""
        for line in decode:
            if line[0:4] == 'http':
                temp += "From Youtube\n"
            else : temp += line + "\n"
        await ctx.send("```\n" + temp + "```")

    @commands.command()
    async def next(self, ctx):
        """Skips the current song"""
        subprocess.run(["mpc", "del", "0"])
        ps = subprocess.Popen(["mpc", "status"], stdout=subprocess.PIPE)
        result = subprocess.run(("head", "-n", "1"), stdin=ps.stdout, stdout=subprocess.PIPE)
        decode = result.stdout.decode('utf-8')
        if decode[0:4] == 'http' : decode = "From Youtube"
        await ctx.send("```\n" + decode + "```")

    @commands.command()
    async def youtube(self, ctx, link: str):
        """Insert a youtube link into the queue."""
        try:
            ps = subprocess.Popen(["yt-dlp", "-f", "140", "-g", link], stdout=subprocess.PIPE)
            subprocess.run(["mpc", "insert"], stdin=ps.stdout, stdout=subprocess.PIPE, check=True)
            await ctx.send("Link Queued.")
        except Exception as e:
            await ctx.send("**`ERROR: %s`**" %  e)

    @commands.command()
    async def reset_stream(self, ctx):
        """Returns to the normal Unicorn Radio Rotation"""
        subprocess.run(["mpc", "crop"])
        subprocess.run(["mpc", "add", "Music/"])
        subprocess.run(["mpc", "shuffle"])
        # Redundant, but helps if I'm being super fucking lazy...
        subprocess.run(["mpc", "play"])
        await ctx.send("Radio returned to normal.")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @tasks.loop(seconds=60)
    async def status_now_playing(self):
        ps = subprocess.Popen(["mpc", "status"], stdout=subprocess.PIPE)
        result = subprocess.run(["head", "-n", "1"], stdin=ps.stdout, stdout=subprocess.PIPE)
        decode = result.stdout.decode('utf-8')
        if decode[0:4] == 'http' : decode = "From Youtube"
        await self.bot.change_presence(activity=discord.Game(name=f'{decode}'))        

async def setup(bot):
    await bot.add_cog(Music(bot))
