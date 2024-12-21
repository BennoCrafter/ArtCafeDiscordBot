import os
import interactions

from src import logutil
from src import data_handler
from src.data_handler import DataHandler
from src.translated_string import TranslatedString

logger = logutil.init_logger(os.path.basename(__file__))

dh = DataHandler.instance()

class Submit(interactions.Extension):
    @interactions.slash_command(
        "submit", description=str(TranslatedString("Submit image to the event"))
    )
    @interactions.slash_option(
        "attachment",
        str(TranslatedString("The image to submit")),
        opt_type=interactions.OptionType.ATTACHMENT,
        required=True,
    )
    async def submit(self, ctx: interactions.SlashContext, attachment: interactions.Attachment):
        await ctx.defer(ephemeral=True)

        current_event = dh.get("current_event")
        if current_event is None:
            await ctx.send(str(TranslatedString("No event is currently running.")), ephemeral=True)
            return

        if current_event["closed"] or current_event["completed"]:
            await ctx.send(str(TranslatedString("Event is already closed.")), ephemeral=True)
            return

        dh.set("current_event.submissions", value=current_event["submissions"] + [{
            "url": attachment.url,
            "author": {
                "name": ctx.author.display_name,
                "id": ctx.author.id
            },
            "submission_id": None,
            "count": 0
        }])

        embed = interactions.Embed(
            title=str(TranslatedString("Submitted!")),
            description=str(TranslatedString("Your image has been submitted!")),
            color=interactions.Color.from_hex("5e50d4"),
        )
        embed.set_image(url=attachment.url)
        await ctx.send(embed=embed, ephemeral=True)
