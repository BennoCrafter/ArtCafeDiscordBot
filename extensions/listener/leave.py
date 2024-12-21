import os

import interactions
from interactions import listen
from interactions.api.events import MemberRemove
from src.config import CONFIG
from src import logutil


logger = logutil.init_logger(os.path.basename(__file__))

class Leave(interactions.Extension):
    """Listen for member leave events."""

    @listen(MemberRemove)
    async def on_member_remove(self, event: MemberRemove):
        # logger.info(f"New member joined: {event.member.display_name}")

        welcome_channel = event.guild.get_channel(CONFIG.channels.welcome)
        if not isinstance(welcome_channel, interactions.GuildText):
            return

        await welcome_channel.send(f"Sadly, {event.member.display_name} has left us. :wave:")
