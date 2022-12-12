import re
import pathlib
import discord
from typing import Optional


from discord.ext import commands
from discord import app_commands


neetcode = pathlib.Path("/home/thinkpad/repos/bots/leetcode")
languages = [x.name for x in neetcode.iterdir() if x.is_dir() and not x.name.startswith(".")]

class Neetcode(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(
        number="the number leetcode problem you want a soluiton for",
        language=", ".join(languages),
    )
    async def leetcode(self, interaction: discord.Interaction, number: int, language: Optional[str] = 'python'):
        """Returns the leetcode solution"""
        files = list(neetcode.glob(language+"/"+str(number)+"-*"))
        if language not in languages or len(files) == 0:
            await interaction.response.send_message(f'there are no solutions for leetcode problem #{number} in {language}')
        
        with open(files[0]) as f:
            code = f.read()

        await interaction.response.send_message(f"```{language}\n{code}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(Neetcode(bot))
