import os

import interactions

from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))


class Ping(interactions.Extension):
    @interactions.slash_command(
        "ping", description="Ping :ping_pong:"
    )
    async def ping(self, ctx: interactions.SlashContext):
        latency = round(self.bot.latency * 1000)
        response = f"Pong! :ping_pong: ({latency}ms latency)"
        await ctx.send(response)
