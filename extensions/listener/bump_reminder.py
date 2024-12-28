import interactions
from interactions.api.events import MessageCreate
from src.logutil import init_logger
import os
import asyncio


logger = init_logger(os.path.basename(__file__))

disboard_id = 302050872383242240

class BumpReminder(interactions.Extension):
    @interactions.listen(MessageCreate)
    async def on_message(self, event: MessageCreate):

        if event.message.author.id != disboard_id:
            return

        logger.info("Bump received!")
        await event.message.add_reaction("❤️")
        # sleep for 2 hours
        await asyncio.sleep(60*60*2)

        await event.message.channel.send(embed=interactions.Embed("Bump Reminder", "It's time to bump the server! :tada:"))
