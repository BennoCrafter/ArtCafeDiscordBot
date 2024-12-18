import os

import interactions
from interactions import listen
from interactions.api.events import MemberAdd

from src import logutil


logger = logutil.init_logger(os.path.basename(__file__))

class Welcome(interactions.Extension):
    """Welcome the user to the server"""

    @listen()
    async def on_member_add(self, event: MemberAdd):
        logger.info(f"New member joined: {event.member.display_name}")
