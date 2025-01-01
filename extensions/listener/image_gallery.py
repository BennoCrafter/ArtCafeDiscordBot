import interactions
from interactions.api.events import MessageCreate
from src.logutil import init_logger
import os
import asyncio
from src.config import CONFIG


logger = init_logger(os.path.basename(__file__))

class ImageGallery(interactions.Extension):
    @interactions.listen(MessageCreate)
    async def on_message(self, event: MessageCreate):
        if len(event.message.attachments) == 0:
            return
        
        if event.channel.id != CONFIG.channel.image_gallery:
            return

        await event.message.add_reaction("❤️")
