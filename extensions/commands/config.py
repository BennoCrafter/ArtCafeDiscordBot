import interactions


class Config(interactions.Extension):
    @interactions.slash_command("config", description="A command to edit the config")
    async def config(self, ctx: interactions.SlashContext):
        await ctx.send(
            components=interactions.spread_to_rows(
                interactions.Button(
                    label="Selector",
                    custom_id="selector",
                    style=interactions.ButtonStyle.PRIMARY,
                ),
                interactions.StringSelectMenu(
                    "Channels Section",
                    "Roles Section",
                    placeholder="I wonder what this does",
                    min_values=1,
                    max_values=2,
                    custom_id="select_me",
                ),
            ),
        )


    @interactions.component_callback("select_me")
    async def select_me(self, ctx: interactions.ComponentContext):
        """A callback for the select me menu"""
        await ctx.send(f"You selected {' '.join(ctx.values)}")
