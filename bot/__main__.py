import asyncio
from pathlib import Path

from discord import LoginFailure
from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or
from discord.ext.commands import command

from bot.constants import Bot as BotConfig


class MusicBot(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_ready(self):
        self.load_extensions()
        print("Ready!")

    def load_extensions(self):
        cogs = Path("./bot/cogs")
        for cog in cogs.iterdir():
            if cog.is_dir():
                continue
            if cog.suffix == ".py" and cog.stem != "__init__":
                path = ".".join(cog.with_suffix("").parts)
                try:
                    self.load_extension(path)
                    print(f"Loading... {path:<22} Success!")
                    #logger.info(f"Loading... {path:<22} Success!")
                except Exception as e:
                    #logger.exception(f"\nLoading... {path:<22} Failed!")
                    print("-"*25)
                    print(f"Loading... {path:<22} Failed!")
                    print(e, "\n", "-"*25, "\n")

    @command()
    async def exit(self, ctx):
        await self.logout()


def run():
    loop = asyncio.get_event_loop()
    params = {
        "command_prefix": when_mentioned_or(BotConfig.prefix),
        "description": "Music bot",
        "loop": loop,
        "case_insensitive": True,
    }

    bot = MusicBot(**params)

    if BotConfig.token is None:
        raise SystemExit("No token provided, exiting")

    try:
        loop.run_until_complete(bot.start(BotConfig.token))

    except (LoginFailure, KeyboardInterrupt):
        loop.run_until_complete(bot.logout())

    finally:
        raise SystemExit("Keyboardinterrup, exiting")


if __name__ == "__main__":
    run()
