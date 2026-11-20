import asyncio
import os

import interactions
from interactions.models import OptionType

from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))

DM_TIMEOUT = 10  # seconds per DM attempt
DM_DELAY = 0.5  # seconds between users


async def dm_members(members, content: str) -> tuple[int, int, int]:
    sent = 0
    failed = 0
    timed_out = 0

    for member in members:
        if member.bot:
            continue

        try:
            await asyncio.wait_for(
                member.user.send(content),
                timeout=DM_TIMEOUT,
            )
            sent += 1

        except asyncio.TimeoutError:
            timed_out += 1
            failed += 1
            logger.warning(f"DM to {member.user.id} timed out after {DM_TIMEOUT}s")

        except Exception as exc:
            failed += 1
            logger.warning(f"Could not DM {member.user.id}: {exc}")

        # Don't hammer Discord with requests
        await asyncio.sleep(DM_DELAY)

    return sent, failed, timed_out


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
    @interactions.slash_option(
        name="role_id",
        description="Role id to which members to send message",
        required=True,
        opt_type=OptionType.STRING,
    )
    async def send_dm(self, ctx, text: str, role_id: str):
        await ctx.defer(ephemeral=True)

        members = [m for m in ctx.guild.members if any(str(role.id) == role_id for role in m.roles)]
        sent, failed, timed_out = await dm_members(members, text)

        await ctx.send(
            f"✅ Sent: `{sent}`\n❌ Failed: `{failed}`\n⏱️ Timed out: `{timed_out}`",
            ephemeral=True,
        )

    @interactions.slash_command(
        name="broadcast",
        description="DM your last message in this channel to every server member",
        default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    )
    async def broadcast(self, ctx: interactions.SlashContext):
        await ctx.defer(ephemeral=True)

        message = None
        async for msg in ctx.channel.history(limit=50):
            if msg.author.id == ctx.author.id and msg.content:
                message = msg
                break

        if message is None:
            await ctx.send("❌ Couldn't find a recent message from you in this channel.", ephemeral=True)
            return

        confirm = interactions.Button(style=interactions.ButtonStyle.SUCCESS, label="Send to everyone", custom_id="broadcast_confirm")
        cancel = interactions.Button(style=interactions.ButtonStyle.DANGER, label="Cancel", custom_id="broadcast_cancel")
        prompt = await ctx.send(
            f"Send this message to **{ctx.guild.member_count}** members?\n>>> {message.content}",
            components=[confirm, cancel],
            ephemeral=True,
        )

        try:
            used = await self.bot.wait_for_component(messages=prompt, components=[confirm, cancel], timeout=60)
        except asyncio.TimeoutError:
            await ctx.edit(prompt, content="⏱️ Timed out, nothing sent.", components=[])
            return

        if used.ctx.custom_id == "broadcast_cancel":
            await used.ctx.edit_origin(content="Cancelled, nothing sent.", components=[])
            return

        await used.ctx.edit_origin(content="📨 Sending...", components=[])
        sent, failed, timed_out = await dm_members(ctx.guild.members, message.content)
        await ctx.edit(
            prompt,
            content=f"✅ Sent: `{sent}`\n❌ Failed: `{failed}`\n⏱️ Timed out: `{timed_out}`",
        )
