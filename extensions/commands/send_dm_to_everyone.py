import os

import interactions
from interactions.models import OptionType

from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))


class SendDmToOptedIn(interactions.Extension):
    @interactions.slash_command(
        name="send_dm",
        description="Send a DM to members who opted in",
        default_member_permissions=interactions.Permissions.MANAGE_MESSAGES,
    )
    @interactions.slash_option(
        name="text",
        description="Message to send",
        required=True,
        opt_type=OptionType.STRING,
    )
    async def send_dm(self, ctx, text: str):
        await ctx.defer(ephemeral=True)

        opt_in_role_id = 1315568418430128158

        sent = 0
        failed = 0

        for member in ctx.guild.members:
            if member.bot:
                continue

            if any(role.id == opt_in_role_id for role in member.roles):
                try:
                    await member.user.send(text)
                    sent += 1
                except Exception as exc:
                    failed += 1
                    logger.warning(f"Could not DM {member.user.id}: {exc}")

        await ctx.send(
            f"✅ Sent: `{sent}`\n❌ Failed: `{failed}`",
            ephemeral=True,
        )
