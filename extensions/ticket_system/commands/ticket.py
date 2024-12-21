import os
import interactions
from src import logutil
from src.config import CONFIG
from src.translated_string import TranslatedString

logger = logutil.init_logger(os.path.basename(__file__))

class Ticket(interactions.Extension):
    @interactions.slash_command(
        "ticket", description=str(TranslatedString("Base command for ticket system"))
    )
    async def ticket(self, ctx: interactions.SlashContext):
        ...

    @ticket.subcommand(
        "setup", sub_cmd_description=str(TranslatedString("Setup ticket system"))
    )
    @interactions.check(
        interactions.has_any_role(CONFIG.roles.staff)
    )
    async def setup(self, ctx: interactions.SlashContext):
        guild = ctx.guild
        if guild is None:
            logger.error("Guild is None")
            await ctx.send(str(TranslatedString("Guild is None")), ephemeral=True)
            return

        ticket_setup_channel = await guild.fetch_channel(CONFIG.channels.ticket_setup)

        if ticket_setup_channel is None or not isinstance(ticket_setup_channel, interactions.GuildText):
            logger.error("Could not find the ticket setup channel")
            await ctx.send(str(TranslatedString("Could not find the ticket setup channel")), ephemeral=True)
            return

        embed = interactions.Embed(
            title=str(TranslatedString("Create a Ticket")),
            description=str(TranslatedString("Click the button below to create a ticket for staff assistance")),
            color=interactions.Color.random()
        )

        button = interactions.Button(
            style=interactions.ButtonStyle.PRIMARY,
            label=str(TranslatedString("Create Ticket")),
            custom_id="create_ticket"
        )

        ticket_setup_message = await ticket_setup_channel.send(embed=embed, components=button)

        await ctx.send(str(TranslatedString("Ticket setup embed: {0}", ticket_setup_channel.mention)), ephemeral=True)

    @interactions.component_callback("create_ticket")
    async def create_ticket(self, ctx: interactions.ComponentContext):
        guild = ctx.guild
        if guild is None:
            logger.error("Guild is None")
            await ctx.send(str(TranslatedString("Guild is None")), ephemeral=True)
            return

        ticket_category = await guild.fetch_channel(CONFIG.channels.tickets_category)

        if ticket_category is None or not isinstance(ticket_category, interactions.GuildCategory):
            logger.error("Could not find the ticket category")
            await ctx.send(str(TranslatedString("Could not find the ticket category")), ephemeral=True)
            return

        channel_name = str(TranslatedString("ticket-{0}", ctx.author.username))
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=ticket_category,
            permission_overwrites=[
                interactions.PermissionOverwrite(
                    id=ctx.author.id,
                    type=interactions.OverwriteType.MEMBER,
                    allow=interactions.Permissions.VIEW_CHANNEL | interactions.Permissions.SEND_MESSAGES
                ),
                interactions.PermissionOverwrite(
                    id=guild.id,
                    type=interactions.OverwriteType.ROLE,
                    deny=interactions.Permissions.VIEW_CHANNEL
                )
            ]
        )

        embed = interactions.Embed(
            title=str(TranslatedString("Ticket Created")),
            description=str(TranslatedString("Thank you for creating a ticket. Staff will assist you shortly.")),
            color=interactions.Color.random()
        )

        close_button = interactions.Button(
            style=interactions.ButtonStyle.DANGER,
            label=str(TranslatedString("Close Ticket")),
            custom_id="close_ticket"
        )

        await ticket_channel.send(
            content=f"<@&{CONFIG.roles.staff}>"
        )
        await ticket_channel.send(
            content=str(TranslatedString("{0} Welcome to your ticket!", ctx.author.mention)),
            embed=embed,
            components=close_button
        )

        await ctx.send(str(TranslatedString("Ticket created: {0}", ticket_channel.mention)), ephemeral=True)

    @interactions.component_callback("close_ticket")
    @interactions.check(
        interactions.has_role(CONFIG.roles.staff)
    )
    async def close_ticket(self, ctx: interactions.ComponentContext):
        await ctx.channel.delete()
