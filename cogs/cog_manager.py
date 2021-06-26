from discord.ext import commands
from random import randint
from cogs.db_manager import adjust_balance_earned


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

    @commands.command(name="coin", help="to toss a coin 0 or 1")
    async def toss_coin(self, ctx, player_roll: int, roll_max: int = 1, bet: int = 0):
        coin_roll = randint(0, roll_max)
        if roll_max > 1:
            coin_roll + 1
        if player_roll == coin_roll and bet > 0:
            bet = bet * 2
            await adjust_balance_earned(self.bot, bet, ctx.author.id, ctx.guild.id)
            await ctx.reply(f'{coin_roll} You won {bet}')
        else:
            bet = bet * -1
            await adjust_balance_earned(self.bot, bet, ctx.author.id, ctx.guild.id)
            await ctx.reply(f'{coin_roll} You lose {bet}')

def setup(bot):
    bot.add_cog(CogCog(bot))
