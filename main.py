import discord
import os
from dotenv import load_dotenv


from discord.ext import commands


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

guild_id = 1017782904509710366  # Replace the 0s with your guild ID.


class Bot(commands.Bot):
    def __init__(self):
        # initialize our bot instance, make sure to pass your intents!
        # for this example, we'll just have everything enabled
        super().__init__(
            command_prefix="?",
            intents=discord.Intents.all(),
            activity=discord.Game(name="☕"),
        )

    # the method to override in order to run whatever you need before your bot starts
    async def setup_hook(self):
        for file in os.listdir(f"./cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await bot.load_extension(f"cogs.{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")


bot = Bot()


@bot.event
async def on_ready():
    # For guild commands
    # await bot.tree.sync(guild=discord.Object(id=guild_id)) # Comment if you are using global commands.
    # await tree.sync() # Uncomment if you want global commands.
    print("Ready!")


bot.run(DISCORD_TOKEN)
