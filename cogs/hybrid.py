# for simplicity, these commands are all global. You can add `guild=` or `guilds=` to `Bot.add_cog` in `setup` to add them to a guild.

import discord
from discord import app_commands
from discord.ext import commands


class MyCog(commands.GroupCog, name="parent"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context.

    @app_commands.command(name="sub-1")
    async def my_sub_command_1(self, interaction: discord.Interaction) -> None:
        """/parent sub-1"""
        await interaction.response.send_message(
            "Hello from sub command 1", ephemeral=True
        )

    @app_commands.command(name="sub-2")
    async def my_sub_command_2(self, interaction: discord.Interaction) -> None:
        """/parent sub-2"""
        await interaction.response.send_message(
            "Hello from sub command 2", ephemeral=True
        )

    @app_commands.describe(
        first_value='The first value you want to add something to',
        second_value='The value you want to add to the first value',
    )
    async def add(interaction: discord.Interaction, first_value: int, second_value: int):
        """Adds two numbers together."""
        await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


async def setup(bot: commands.Bot) -> None:
    # await bot.add_cog(MyCog(bot))
    await bot.add_cog(MyCog(bot), guilds=[discord.Object(id=1017782904509710366)])
