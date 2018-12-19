import discord

from discord import ClientException
from discord.ext import commands


class Tools:
    def __init__(self, bot):
        self.bot = bot

    async def invoke(self, ctx, cmd_name, *args, **kwargs):
        """
        Invokes a command with args and kwargs.
        Fail early through `command.can_run`, and logs warnings.
        :param ctx: Context instance for command call
        :param cmd_name: Name of command/subcommand to be invoked
        :param args: args to be passed to the command
        :param kwargs: kwargs to be passed to the command
        """

        #log.debug(f"{cmd_name} was invoked through an alias")
        cmd = self.bot.get_command(cmd_name)
        if not cmd:
            # log.warning(f'Did not find command "{cmd_name}" to invoke.')
            return
        elif not await cmd.can_run(ctx):
            return  # log.warning(
            #f'{str(ctx.author)} tried to run the command "{cmd_name}"'
            # )

        await ctx.invoke(cmd, *args, **kwargs)

    @commands.group(name="cog", aliases=("cogs",))
    async def cogs_group(self, ctx):
        pass

    @cogs_group.command(name="load", aliases=("l",))
    async def load_cog(self, ctx, cog_name):
        if not "bot.cogs." in cog_name:
            cog_name = f"bot.cogs.{cog_name}"

        try:
            self.bot.load_extension(cog_name)
            await ctx.send(f"Successfully loaded {cog_name}")

        except (ClientException, ImportError) as e:
            await ctx.send(
                f"Something went wrong when loading {cog_name}"
                f"```{e}```"
            )

    @cogs_group.command(name="unload", aliases=("u",))
    async def unload_cog(self, ctx, cog_name):
        if cog_name.lower() == "tools":
            return await ctx.send("Can not unload the tools cog, use reload.")

        if not "bot.cogs." in cog_name:
            cog_name = f"bot.cogs.{cog_name}"

        try:
            self.bot.unload_extension(cog_name)
            await ctx.send(f"Successfully unloaded {cog_name}")

        except (ClientException, ImportError) as e:
            await ctx.send(
                f"Something went wrong when unloading {cog_name}"
                f"```{e}```"
            )

    @cogs_group.command(name="reload", alises=("r",))
    async def reload_cog(self, ctx, cog_name):
        if not "bot.cogs." in cog_name:
            cog_name = f"bot.cogs.{cog_name}"

        try:
            self.bot.unload_extension(cog_name)
            await ctx.send(f"Successfully unloaded {cog_name}")

        except (ClientException, ImportError) as e:
            return await ctx.send(
                f"Something went wrong when unloading {cog_name}"
                f"```{e}```"
            )

        try:
            self.bot.load_extension(cog_name)
            await ctx.send(f"Successfully loaded {cog_name}")

        except (ClientException, ImportError) as e:
            await ctx.send(
                f"Something went wrong when loading {cog_name}"
                f"```{e}```"
            )

    @cogs_group.command(name="list")
    async def get_cogs(self, ctx):
        await ctx.send(", ".join(list(self.bot.cogs)))

    @commands.command(name="load")
    async def alias_load_cog(self, ctx, cog):
        await self.invoke(ctx, "cog load", cog)

    @commands.command(name="unload")
    async def alias_unload_cog(self, ctx, cog):
        await self.invoke(ctx, "cog unload", cog)

    @commands.command(name="reload")
    async def alias_reload_cog(self, ctx, cog):
        await self.invoke(ctx, "cog reload", cog)

    @commands.command(name="cogslist")
    async def alias_list_cogs(self, ctx):
        await self.invoke(ctx, "cog list")


def setup(bot):
    bot.add_cog(Tools(bot))
