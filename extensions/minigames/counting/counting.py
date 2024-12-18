import os

import interactions
from interactions import listen
from interactions.api.events import MessageCreate

from src import logutil
from src.config import CONFIG


logger = logutil.init_logger(os.path.basename(__file__))


class CountingMinigame(interactions.Extension):
    @listen(MessageCreate)
    async def on_message_create(self, event: MessageCreate):
        if event.message.channel.id != CONFIG.channels.counting:
            return
