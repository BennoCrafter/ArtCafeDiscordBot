import os

import interactions
from interactions import listen
from interactions.api.events import MemberRemove
from src.config import CONFIG
from src import logutil
from src.translated_string import TranslatedString


logger = logutil.init_logger(os.path.basename(__file__))

class Leave(interactions.Extension):
    """Listen for member leave events."""

    @listen(MemberRemove)
    async def on_member_remove(self, event: MemberRemove):
        # logger.info(f"New member joined: {event.member.display_name}")

        welcome_channel = event.guild.get_channel(CONFIG.channels.welcome)
        if not isinstance(welcome_channel, interactions.GuildText):
            return

        await welcome_channel.send(str(TranslatedString("Sadly, {0} has left us. :wave:", event.member.display_name)))
