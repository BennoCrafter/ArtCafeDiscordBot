
import os

import interactions

from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))


class Submit(interactions.Extension):
    @interactions.slash_command(
        "submit", description="Submit image to the event"
    )
    @interactions.slash_option(
        "attachment",
        "The image to submit",
        opt_type=interactions.OptionType.ATTACHMENT,
        required=True,
    )
    async def submit(self, ctx: interactions.SlashContext, attachment: interactions.Attachment):
        embed: interactions.Embed = interactions.Embed(
            title="Submitted!",
            description="Your image has been submitted!",
            color=interactions.Color.from_hex("5e50d4"),
        )
        embed.set_image(url=attachment.url)
        await ctx.send(embed=embed, ephemeral=True)
