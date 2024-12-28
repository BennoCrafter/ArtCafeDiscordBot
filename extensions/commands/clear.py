import os
import interactions
from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))

class Clear(interactions.Extension):

    @interactions.slash_command(
        name="clear",
        description="clears messages",
        default_member_permissions=interactions.Permissions.MANAGE_MESSAGES,
    )
    @interactions.slash_option(
        name="count",
        description="number of messages to clear",
        required=True,
        opt_type=interactions.OptionType.INTEGER,
        max_value=100,
        min_value=2,
    )
    @interactions.slash_option(
        name="user",
        description="user to clear messages from",
        required=False,
        opt_type=interactions.OptionType.USER,
    )
    async def clear(self, ctx, count, user=None):
        reason = f"@{ctx.author.display_name}({ctx.author.id}) cleared {count} messages"
        if user:
            await ctx.channel.purge(
                deletion_limit=count,
                predicate=lambda m: m.author == user,
                reason=reason,
            )
        if user == None:
            await ctx.channel.purge(deletion_limit=count)
            user = "`All`"
        elif user:
            user = user.mention
        embed = interactions.Embed(
            title="Messages deleted successfully",
            description=f"> `{count}` messages deleted succesfully",
            color=interactions.Color.from_hex("5e50d4"),
        )
        await ctx.send(embed=embed, ephemeral=True)
