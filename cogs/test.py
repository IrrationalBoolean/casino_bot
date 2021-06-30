from discord.ext import commands
import discord
import random
from PIL import Image
from classes.blackjack import BlackJackHand


import io


async def draw(image: Image, ctx):
    """sends image object to channel ctx comes from as a png"""
    with io.BytesIO() as ib:
        image.save(ib, 'PNG')
        ib.seek(0)
        return await ctx.channel.send(file=discord.File(ib, 'card.png'))


class TestCog(commands.Cog, name="Testing"):
    def __init__(self, bot):
        self.bot = bot
    #
    # @commands.command(name="test")
    # async def test(self, ctx, *card):
    #     await ctx.reply(f"{' '.join(card)}")

    @commands.command(name="card")
    async def card(self, ctx, card, deck=None):
        print(card)
        if deck is None:
            deck = random.choice(["byron_knoll", "dice_trumps"])
        if card.lower() in ["random", "r", ""]:
            card = random.choice([f"{y}{x}" for x in list(range(2, 11)) + list('AJQK') for y in list("SHDC")])
        img = self.bot.decks[deck][card.upper()]
        await draw(img, ctx)

    @commands.command(name="hand", help="delivers requested hand")
    async def hand(self, ctx, cards = None, deck=None):
        if cards is None:
            cards = ["SA", "SK", "SQ", "SJ", "S10"]
        if len(cards[0]) == 1:
            cards = ''.join(cards).upper().split('.')
        if deck is None:
            deck = random.choice(["byron_knoll", "dice_trumps"])
        d = self.bot.decks[deck]
        width, height = d["SA"].size
        total_width = width + ((len(cards) - 1) * ((width // 3) * 2))
        table = Image.new("RGBA", (total_width, height), (0, 0, 0, 0))
        for idx, image in enumerate(cards):
            x_y = (idx * (width // 3 * 2), 0)
            table.paste(d[image], x_y, d[image])

        await draw(table, ctx)

    @commands.command(name="decks")
    async def decks(self, ctx):
        embed = discord.Embed(title="Available Styles", description=f"`{'`, `'.join(self.bot.decks.keys())}`",
                              color=0x992d22)
        await ctx.channel.send(embed=embed)



    @commands.command(name="count")
    async def count(self, ctx, hand):
        cards = hand.split('.')
        player_hand = BlackJackHand()
        for card in cards:
            player_hand += card.upper()
        await ctx.reply(f"Your hand is valued at {player_hand.tabulate_score()}")




def setup(bot):
    bot.add_cog(TestCog(bot))
