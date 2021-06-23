from discord.ext import commands
from dotenv import dotenv_values

dotenv = dotenv_values(".env")
TOKEN = dotenv["TOKEN"]
bot = commands.Bot(command_prefix="~")
bot.load_extension("cogs.cog_manager")

bot.run(TOKEN)
