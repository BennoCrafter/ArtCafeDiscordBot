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
            embed = interactions.Embed(
                title="It seems like you mentioned me",
                description="".join(
                    [
                        "I could not help much but noticed you mentioned me.",
                        f"You can type ``/`` and choose **{self.bot.user.username}**",
                        " to start using me. Alternatively, you can use ",
                        "`$help` or `/help` to see a list of available ",
                        "commands. Thank you for choosing Articuno.",
                    ],
                ),
                color=0x6AA4C1,
            )
            await msg.channel.send(embeds=embed)
