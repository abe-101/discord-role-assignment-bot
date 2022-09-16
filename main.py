import os, re, discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True


bot = commands.Bot(command_prefix="!", intents=intents)


async def dm_about_roles(member):
    print(f"DMing {member.name}...")

    await member.send(
        f"""Hi {member.name}, welcome to {member.guild.name}!

Which chapter would you like to be part of:

* NYC (🐍)
* Chicago (🕸️)

Reply to this message with one or more of the city's or emojis above so I can assign you the right roles on our server.

Reply with the name or emoji of a city you're currently using and want to stop and I'll remove that role for you.
"""
    )


async def assign_roles(message):
    print("Assigning roles...")

    languages = set(re.findall("nyc|chicago", message.content, re.IGNORECASE))
    language_emojis = set(re.findall("\U0001F40D|\U0001F578", message.content))
    # https://unicode.org/emoji/charts/full-emoji-list.html

    # Convert emojis to names
    for emoji in language_emojis:
        {
            "\U0001F40D": lambda: languages.add("nyc"),
            "\U0001F578": lambda: languages.add("chicago"),
        }[emoji]()

    if languages:
        server = bot.get_guild(SERVER_ID)

        new_roles = set(
            [
                discord.utils.get(server.roles, name=language.lower())
                for language in languages
            ]
        )

        member = await server.fetch_member(message.author.id)

        current_roles = set(member.roles)
        roles_to_add = new_roles.difference(current_roles)
        roles_to_remove = new_roles.intersection(current_roles)

        try:
            await member.add_roles(
                *roles_to_add, reason="Roles assigned by WelcomeBot."
            )
            await member.remove_roles(
                *roles_to_remove, reason="Roles revoked by WelcomeBot."
            )
        except Exception as e:
            print(e)
            await message.channel.send("Error assigning/removing roles.")
        else:
            if roles_to_add:
                await message.channel.send(
                    f"You've been assigned the following role{'s' if len(roles_to_add) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_add]) }"
                )

            if roles_to_remove:
                await message.channel.send(
                    f"You've lost the following role{'s' if len(roles_to_remove) > 1 else ''} on {server.name}: { ', '.join([role.name for role in roles_to_remove]) }"
                )


@bot.event
async def on_member_join(member):
    await dm_about_roles(member)


@bot.event
async def on_message(message):
    print("Saw a message...")

    if message.author == bot.user:
        return  # prevent responding to self

    # Assign roles from DM
    if isinstance(message.channel, discord.channel.DMChannel):
        await assign_roles(message)
        return

    # Respond to commands
    if message.content.startswith("!roles"):
        await dm_about_roles(message.author)
    elif message.content.startswith("!serverid"):
        await message.channel.send(message.channel.guild.id)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


bot.run(DISCORD_TOKEN)
