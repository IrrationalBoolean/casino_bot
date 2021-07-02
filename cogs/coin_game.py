from discord.ext import commands
from random import randint

from cogs.db_manager import adjust_balance_earned


class Coin_Game(commands.Cog, name="Coin Game"):
    def __init__(self, bot) -> None:
        super().__init__()

        self.bot = bot

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
    bot.add_cog(Coin_Game(bot))