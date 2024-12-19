import os

import interactions

from src import logutil
from src.config import CONFIG


logger = logutil.init_logger(os.path.basename(__file__))


class Ticket(interactions.Extension):
    @interactions.slash_command(
        "ticket", description="Base command for ticket system"
    )
    async def ticket(self, ctx: interactions.SlashContext):
        ...

    @ticket.subcommand(
        "setup", sub_cmd_description="Setup ticket system"
    )
    @interactions.check(
        interactions.has_any_role(CONFIG.roles.staff)
    )
    async def setup(self, ctx: interactions.SlashContext):
        guild = ctx.guild
        if guild is None:
            logger.error("Guild is None")
            await ctx.send("Guild is None", ephemeral=True)
            return

        ticket_setup_channel = await guild.fetch_channel(CONFIG.channels.ticket_setup)

        if ticket_setup_channel is None or not isinstance(ticket_setup_channel, interactions.GuildText):
            logger.error("Could not find the ticket setup channel")
            await ctx.send("Could not find the ticket setup channel", ephemeral=True)
            return

        embed = interactions.Embed(
            title="Create a Ticket",
            description="Click the button below to create a ticket for staff assistance",
            color=interactions.Color.random()
        )

        button = interactions.Button(
            style=interactions.ButtonStyle.PRIMARY,
            label="Create Ticket",
            custom_id="create_ticket"
        )

        ticket_setup_message = await ticket_setup_channel.send(embed=embed, components=button)

        await ctx.send(f"Ticket setup embed: {ticket_setup_channel.mention}", ephemeral=True)

    @interactions.component_callback("create_ticket")
    async def create_ticket(self, ctx: interactions.ComponentContext):
        guild = ctx.guild
        if guild is None:
            logger.error("Guild is None")
            await ctx.send("Guild is None", ephemeral=True)
            return

        ticket_category = await guild.fetch_channel(CONFIG.channels.tickets_category)

        if ticket_category is None or not isinstance(ticket_category, interactions.GuildCategory):
            logger.error("Could not find the ticket category")
            await ctx.send("Could not find the ticket category", ephemeral=True)
            return

        channel_name = f"ticket-{ctx.author.username}"
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
            title="Ticket Created",
            description=f"Thank you for creating a ticket. Staff will assist you shortly.",
            color=interactions.Color.random()
        )

        close_button = interactions.Button(
            style=interactions.ButtonStyle.DANGER,
            label="Close Ticket",
            custom_id="close_ticket"
        )

        await ticket_channel.send(
            content=f"{ctx.author.mention} Welcome to your ticket!",
            embed=embed,
            components=close_button
        )

        await ctx.send(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

    @interactions.component_callback("close_ticket")
    @interactions.check(
        interactions.has_any_role(CONFIG.roles.staff)
    )
    async def close_ticket(self, ctx: interactions.ComponentContext):
        await ctx.channel.delete()
        await ctx.author.send("Ticket has been closed.")
