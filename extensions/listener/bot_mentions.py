import os

import interactions
from interactions import listen
from interactions.api.events import MessageCreate

from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))


class BotMentions(interactions.Extension):
    """Listen for bot mentions."""

    @listen(MessageCreate)
    async def bot_mentions(self, event: MessageCreate) -> None:
        """Check for bot mentions."""
        msg = event.message
        if (
            f"@{self.bot.user.id}" in msg.content
            or f"<@{self.bot.user.id}>" in msg.content
        ):
            await msg.channel.send("What's up? :smile:")
