import os

import interactions

from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))


class TemplateCog(interactions.Extension):
    @interactions.slash_command(
        "test", description="test command"
    )
    async def test_cmd(self, ctx: interactions.SlashContext):
        """Register as an extension command"""
        await ctx.send("Test")
