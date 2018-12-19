import functools
from collections import deque
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import command
import youtube_dl

from concurrent.futures import ThreadPoolExecutor

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'audio_cache/%(extractor)s-%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'usenetrc': True
}

youtube_dl.utils.bug_reports_message = lambda: ''


class Music:
    def __init__(self, bot):
        self.bot = bot

        if not Path("ffmpeg/bin/ffmpeg.exe").exists:
            self.bot.remove_cog(self)
            print("FFMPEG.exe was not found, music cog was unloaded")

        self.clients = {}
        self.queue = deque()
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        self.yt_dl = youtube_dl.YoutubeDL(ytdl_format_options)

        self.check_voice_clients()

    def check_voice_clients(self):
        for vc in self.bot.voice_clients:
            self.clients[vc.guild.id] = vc

    @command()
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        channel = channel or ctx.author.voice.channel

        try:
            self.clients[ctx.guild.id] = await channel.connect()
        except discord.ClientException:
            await self.clients[ctx.guild.id].disconnect()
            self.clients[ctx.guild.id] = await channel.connect()

    @command()
    async def play(self, ctx, song):
        voice = self.clients.get(ctx.guild.id)

        if not voice:
            try:
                voice = await ctx.author.voice.channel.connect()
                self.clients[ctx.guild.id] = voice
            except:
                return await ctx.send("I'm not in a voice channel, and could not join yours")

        result = await self.bot.loop.run_in_executor(
            self.thread_pool,
            functools.partial(self.yt_dl.extract_info, download=True, url=song)
        )

        #from pprint import pprint
        # pprint(result)
        name = f"audio_cache/youtube-{result['display_id']}.webm"

        source = discord.FFmpegPCMAudio(
            name,
            executable="ffmpeg/bin/ffmpeg.exe"
        )
        volume_source = discord.PCMVolumeTransformer(source, volume=0.5)

        voice.play(volume_source, after=lambda: print("done playing"))


def setup(bot):
    bot.add_cog(Music(bot))
