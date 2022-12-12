import re
import discord
from discord.ext import commands



class Main(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if re.fullmatch(rf"<@!?{self.bot.user.id}>", message.content):
            em = discord.Embed(
                description=f'Hello! My prefix is `?`',
                color=discord.Color.random(),
            )
            await message.reply(embed=em)


async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
