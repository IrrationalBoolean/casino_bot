from discord.ext import commands
from dotenv import dotenv_values
from utils.deck_loader import load_decks


on_start_cogs = ["cog_manager", "db_manager"]
dotenv = dotenv_values(".env")
TOKEN = dotenv["TOKEN"]
bot = commands.Bot(command_prefix="<>")
bot.decks = load_decks()
for c in on_start_cogs:
    bot.load_extension(f"cogs.{c}")
bot.run(TOKEN)
