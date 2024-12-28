import os
import interactions
from src.logutil import init_logger
from src.config import CONFIG
from datetime import datetime
from src.data_handler import DataHandler
from src.translated_string import TranslatedString


logger = init_logger(os.path.basename(__file__))
dh = DataHandler.instance()


class Event(interactions.Extension):

    @interactions.slash_command(
        "event", description=str(TranslatedString("Base Event command"))
    )
    async def event(self, ctx: interactions.SlashContext):
        ...

    @interactions.check(
        interactions.has_any_role(CONFIG.roles.staff)
    )
    @event.subcommand(
        "create", sub_cmd_description=str(TranslatedString("Command to create an event"))
    )
    @interactions.slash_option(
        "name", str(TranslatedString("Name of the event")), required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        "description", str(TranslatedString("Description of the event")), required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        "end_date", str(TranslatedString("End date of the event")), required=True,
        opt_type=interactions.OptionType.STRING
    )
    async def create(self, ctx: interactions.SlashContext, name: str, description: str, end_date: str):
        await ctx.send(str(TranslatedString("Creating an event")), ephemeral=True)

        try:
            parsed_date: datetime = datetime.strptime(end_date, "%d.%m.%Y")
        except ValueError:
            await ctx.send(str(TranslatedString("Invalid date format. Use DD.MM.YYYY")), ephemeral=True)
            return

        channel = self.get_channel(ctx, CONFIG.channels.event_info)
        if channel is None:
            logger.error("Could not find the event info channel")
            await ctx.send(str(TranslatedString("Could not find the event info channel")), ephemeral=True)
            return

        dh.set("current_event", value={"name": name, "description": description, "end_date": end_date, "closed": False, "completed": False, "submissions": []})
        e = interactions.Embed(title=name, description=description, color=interactions.Color.random(), footer=interactions.EmbedFooter(text=f"Ends: {end_date}"))
        await channel.send(str(TranslatedString("🎉 New Event started! 🎉")))
        await channel.send(embed=e)

    @event.subcommand(
        "close", sub_cmd_description=str(TranslatedString("Command to close an event"))
    )
    async def close(self, ctx: interactions.SlashContext):
        current_event = dh.get("current_event")

        if current_event is None:
            await ctx.send(str(TranslatedString("No event is currently running")), ephemeral=True)
            return
        if current_event["closed"]:
            await ctx.send(str(TranslatedString("Event is already closed")), ephemeral=True)
            return

        await ctx.send(str(TranslatedString("Closing event")), ephemeral=True)
        dh.set("current_event.closed", value=True)

        embeds = self.generate_embeds(current_event)

        channel = self.get_channel(ctx, CONFIG.channels.event_info)
        if channel is None:
            logger.error("Could not find the event info channel")
            await ctx.send(str(TranslatedString("Could not find the event info channel")), ephemeral=True)
            return

        await channel.send(str(TranslatedString("# Event has ended!")))
        event_channel = self.get_channel(ctx, CONFIG.channels.event_info)
        if event_channel is None:
            logger.error("Could not find the event vote channel")
            await ctx.send(str(TranslatedString("Could not find the event vote channel")), ephemeral=True)
            return

        for embed, e in zip(embeds, current_event["submissions"]):
            msg = await event_channel.send(embed=embed)
            current_event = dh.get("current_event")
            current_event["submissions"][embeds.index(embed)]["submission_id"] = msg.id
            dh.set("current_event", current_event)
            await msg.add_reaction("⭐")

    @event.subcommand(
        "results", sub_cmd_description=str(TranslatedString("Command to show results of current event"))
    )
    async def results(self, ctx: interactions.SlashContext):
        current_event = dh.get("current_event")

        if current_event is None:
            await ctx.send(str(TranslatedString("No event is currently running")), ephemeral=True)
            return

        if not current_event["closed"]:
            await ctx.send(str(TranslatedString("Event is not yet closed")), ephemeral=True)
            return

        embeds = self.generate_embeds(current_event)
        event_channel = self.get_channel(ctx, CONFIG.channels.event_info)
        if event_channel is None:
            logger.error("Could not find the event vote channel")
            await ctx.send(str(TranslatedString("Could not find the event vote channel")), ephemeral=True)
            return

        sorted_data = sorted(current_event["submissions"], key=lambda x: x["count"], reverse=True)
        emojis = ["🥇", "🥈", "🥉"]
        top_winners = sorted_data[:3]
        honorable_mentions = sorted_data[3:]

        # Build podium text
        podium_lines = []
        for i, winner in enumerate(top_winners):
            emoji = emojis[i]
            podium_lines.append(f"{emoji} **{winner["author"]["name"]}** - {winner['count']}")

        # Add honorable mentions
        honorable_lines = []
        for rank, participant in enumerate(honorable_mentions, start=4):
            honorable_lines.append(f"🎖️ **{rank}. {participant['author']['name']}** - {participant['count']}")

        embed = interactions.Embed(
            title=str(TranslatedString("🏆 Winners' Podium 🏆")),
            color=0xFFD700
        )
        embed.add_field(name=str(TranslatedString("🥳 Top Winners")), value="\n".join(podium_lines), inline=False)

        if honorable_lines:
            embed.add_field(name=str(TranslatedString("🎖️ Honorable Mentions")), value="\n".join(honorable_lines), inline=False)

        embed.set_footer(text=str(TranslatedString("✨ Celebrate the champions! ✨")))
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/904269851302686730.png")

        await ctx.send(str(TranslatedString("Sending podium")), ephemeral=True)
        await event_channel.send(embed=embed)


    @staticmethod
    def generate_embeds(current_event: dict) -> list[interactions.Embed]:
        embeds: list[interactions.Embed] = []

        for submission in current_event["submissions"]:
            e = interactions.Embed(
                title=f"Submission by: {submission['author']["name"]}",
                color=interactions.Color.from_hex("5D576B"),
            )
            e.set_image(url=submission["url"])
            embeds.append(e)
        return embeds

    @staticmethod
    def get_channel(ctx: interactions.SlashContext, channel_id: int) -> interactions.GuildText | None:
        guild = ctx.guild

        if guild is None:
            return None
        channel = guild.get_channel(CONFIG.channels.event_info)

        if channel is None:
            return None

        if not isinstance(channel, interactions.GuildText):
            return None

        return channel

    @staticmethod
    def is_reaction_for_event(event: interactions.events.MessageReactionAdd, submissions: list[dict]) -> bool:
        if event.author.bot:
            return False
        if event.message.channel.id != CONFIG.channels.event_info:
            return False
        if event.emoji.name != "⭐":
            return False

        for submission in submissions:
            if int(event.message.id) == submission["submission_id"]:
                return True

        return False

    @staticmethod
    def change_submission_count(submissions: list[dict], submisson_id: int, count: int):
        for submission in submissions:
            if submisson_id == submission["submission_id"]:
                submission["count"] = submission.get("count", 0) + count
                dh.set("current_event.submissions", submissions)
                break
