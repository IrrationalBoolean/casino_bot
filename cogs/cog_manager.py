from discord.ext import commands


class CogCog(commands.Cog, name="Cog Controls"):
    def __init__(self, bot):
        self.bot = bot

    def load_cog(self, extension):
        self.bot.load_extension(f"cogs.{extension}")

    def unload_cog(self, extension):
        if extension == "cog_manager":
            return
        self.bot.unload_extension(f"cogs.{extension}")

    @commands.command(name="reload", help="reloads cog")
    async def reload(self, ctx, extension):
        self.unload_cog(extension)
        msg = await ctx.reply(f"{extension} has been unloaded")
        self.load_cog(extension)
        await msg.edit(content=f"{extension} has been reloaded")

    @commands.command(name="load", help="loads cog")
    async def load(self, ctx, extension):
        self.load_cog(extension)
        await ctx.reply(f"{extension} has been loaded")

    @commands.command(name="unload", help="unloads cog")
    async def unload(self, ctx, extension):
        self.unload_cog(extension)
        await ctx.reply(f"{extension} has been unloaded")


def setup(bot):
    bot.add_cog(CogCog(bot))
