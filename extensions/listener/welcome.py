import os

import interactions
from interactions import listen
from interactions.api.events import MemberAdd
from src.config import CONFIG
from src import logutil
from src.translated_string import TranslatedString


logger = logutil.init_logger(os.path.basename(__file__))

class Welcome(interactions.Extension):
    """Welcome the user to the server"""

    @listen()
    async def on_member_add(self, event: MemberAdd):
        # logger.info(f"New member joined: {event.member.display_name}")

        embed = interactions.Embed(
            title=str(TranslatedString("Welcome, {0}", event.member.display_name)),
            description=str(TranslatedString("Welcome on Art Cafe! Have fun and enjoy your stay!")),
            color=interactions.Color.from_hex("ba6e5e")
        )

        embed.set_thumbnail(url=event.member.avatar.url)

        role = event.guild.get_role(CONFIG.roles.member)
        welcome_channel = event.guild.get_channel(CONFIG.channels.welcome)
        if not isinstance(welcome_channel, interactions.GuildText):
            return

        await welcome_channel.send(embeds=embed)
        # logger.info(f"Sent welcome message for {event.member.display_name}")

        if not role:
            return

        await event.member.add_role(role)
        # logger.info(f"Added role {role.name} to {event.member.display_name}")
