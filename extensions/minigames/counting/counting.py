import os

import interactions
from interactions import Member, User, listen
from interactions.api.events import MessageCreate
from interactions.models.internal import command

from src import logutil
from src.config import CONFIG
from src.data_handler import DataHandler
from src.translated_string import TranslatedString

logger = logutil.init_logger(os.path.basename(__file__))
dh = DataHandler.instance()


class CountingMinigame(interactions.Extension):
    current_count: int = dh.get("minigames.counting.count", 0)
    prev_message_author: Member | User | None = None

    @listen(MessageCreate)
    async def on_message_create(self, event: MessageCreate):
        if event.message.channel.id != CONFIG.channels.counting:
            return
        if event.message.author == self.bot.user:
            return

        try:
            result = eval(event.message.content)

            if not isinstance(result, (int, float)):
                return
        except:
            return

        result = int(result)

        if event.message.author.id == self.prev_message_author:
            await self.error_reaction(event)
            return

        if result == self.current_count + 1:
            await self.success_reaction(event)
            self.prev_message_author = event.message.author
            return

        await self.error_reaction(event)
        return

    async def error_reaction(self, event: MessageCreate):
        self.current_count = 0
        dh.set("minigames.counting.count", value=0)
        self.prev_message_author = None

        await event.message.add_reaction(":x:")

    async def success_reaction(self, event: MessageCreate):
        self.current_count += 1
        dh.set("minigames.counting.count", value=self.current_count)
        await event.message.add_reaction(":white_check_mark:")

    @interactions.slash_command(
        "count", description=str(TranslatedString("Base Counting command"))
    )
    async def count(self, event: MessageCreate): ...

    @interactions.check(interactions.has_any_role(CONFIG.roles.staff))
    @count.subcommand(
        "set", sub_cmd_description=str(TranslatedString("Command to set the count"))
    )
    @interactions.slash_option(
        "count",
        str(TranslatedString("Count to set")),
        required=True,
        opt_type=interactions.OptionType.INTEGER,
    )
    async def set(self, ctx: interactions.SlashContext, count: int):
        self.current_count = count
        dh.set("minigames.counting.count", value=count)
        await ctx.send(f"Count set to {count}")
