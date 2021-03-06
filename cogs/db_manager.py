from discord.ext import commands
import aiosqlite
# from utils.qualifier import make_table
#
#
# async def return_leaderboard(bot, guild_id):
#     async with bot.db.execute("SELECT user_id, balance, total_earnings, total_losses FROM user "
#                               "WHERE guild_id = ? ORDER BY balance DESC LIMIT 5",
#                               (guild_id,)) as cursor:
#         rows = await cursor.fetchall()
#         new_rows = [[await bot.fetch_user(row[0]) , *row[1:]] for row in rows]
#         for item in new_rows:
#             item[0] = item[0].display_name
#         return "```" + make_table(rows=new_rows, labels=["ID","Wallet","Profits","Losses"], centered=True) + "```"


async def connect_to_db(bot):
    """called at bot on_ready, creates bot.db connection to casino_data.db"""
    bot.db = await aiosqlite.connect("casino_data.db")
    await bot.db.execute(
        "CREATE TABLE IF NOT EXISTS user (guild_id int, user_id int, balance int, "
        "total_earnings int, total_losses int, PRIMARY KEY (guild_id, user_id))")


async def adjust_balance_earned(bot, amount, user_id, guild_id):
    if amount > 0:
        win = amount
        loss = 0
    else:
        win = 0
        loss = amount
    cursor = await bot.db.execute("INSERT OR IGNORE INTO user(guild_id, user_id, "
                                  "balance, total_earnings, total_losses) "
                                  "VALUES (?,?,?,?,?)",
                                  (guild_id, user_id, amount, win, loss))
    if cursor.rowcount == 0:
        if win:
            await bot.db.execute(f"UPDATE user SET balance = balance + ?, total_earnings = total_earnings + ? "
                                 "WHERE guild_id = ? and user_id = ?",
                                 (amount, amount, guild_id, user_id))
        else:
            await bot.db.execute(f"UPDATE user SET balance = balance + ?, total_losses = total_losses + ? "
                                 "WHERE guild_id = ? and user_id = ?",
                                 (amount, amount, guild_id, user_id))
    cur = await bot.db.execute("SELECT balance, total_earnings, total_losses FROM user "
                               "WHERE guild_id = ? and user_id = ?",
                               (guild_id, user_id))
    balance = await cur.fetchone()
    await bot.db.commit()
    return balance


async def adjust_balance(bot, amount, user_id, guild_id):
    cursor = await bot.db.execute("INSERT OR IGNORE INTO user(guild_id, user_id, "
                                  "balance, total_earnings, total_losses) "
                                  "VALUES (?,?,?,?,?)",
                                  (guild_id, user_id, amount, 0, 0))
    if cursor.rowcount == 0:
        await bot.db.execute("UPDATE user SET balance = balance + ? WHERE guild_id = ? and user_id = ?",
                             (amount, guild_id, user_id))
    await bot.db.commit()


async def get_balance(bot, user_id, guild_id):
    cursor = await bot.db.execute("SELECT balance, total_earnings, total_losses "
                                  "FROM user WHERE guild_id = ? and user_id =?",
        (guild_id, user_id))
    bal = await cursor.fetchone()
    if bal:
        return bal
    else:
        return None



class DatabaseCog(commands.Cog, name="DatabaseCog"):
    def __init__(self, bot):
        self.bot = bot

    # await ctx.channel.send(await return_leaderboard(self.bot, ctx.guild.id))

    @commands.command()
    async def earn(self, ctx, amount: int):
        if amount > 1000:
            amount = 1000
        if amount < -1000:
            amount = -1000
        await adjust_balance_earned(self.bot, amount, ctx.author.id, ctx.guild.id)

    @commands.command()
    async def get(self, ctx, amount: int):
        if amount > 1000:
            amount = 1000
        if amount < -1000:
            amount = -1000
        await adjust_balance(self.bot, amount, ctx.author.id, ctx.guild.id)

    @commands.command()
    async def bal(self, ctx):
        bal = await get_balance(self.bot, ctx.author.id, ctx.guild.id)
        if bal:
            await ctx.channel.send(f"Current balance is {bal[0]}, lifetime earn: {bal[1]}, lifetime loss: {bal[2]}")
        else:
            await ctx.channel.send("You have no balance history in this guild.")

    async def take(self):
        pass


def setup(bot):
    bot.add_cog(DatabaseCog(bot))
