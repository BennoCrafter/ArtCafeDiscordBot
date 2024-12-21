import os

import interactions

from src import logutil
from src.config import CONFIG


logger = logutil.init_logger(os.path.basename(__file__))


class SetupRules(interactions.Extension):
    @interactions.slash_command(
        "setup", description="base command"
    )
    async def setup(self, ctx: interactions.SlashContext):
        ...

    @setup.subcommand(
        "rules", sub_cmd_description="Setup rules"
    )
    @interactions.slash_option(
        "rules",
        "The rules to set",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def rules(self, ctx: interactions.SlashContext, rules: str):
        guild = ctx.guild
        if guild is None:
            logger.error("Guild is None")
            await ctx.send("Guild is None", ephemeral=True)
            return

        rules_channel = await guild.fetch_channel(CONFIG.channels.rules)

        if rules_channel is None or not isinstance(rules_channel, interactions.GuildText):
            logger.error("Could not find the rules_channel")
            await ctx.send("Could not find the rules_channel", ephemeral=True)
            return

        await ctx.send("Sending rules...", ephemeral=True)

        embed = interactions.Embed(title="Rules 📗", color=0x00ff00)
        rules_list = str(rules).split("\n")
        for i, rule in enumerate(rules_list):
            print(rule)
            embed.add_field(name=f"{i}.", value=rule.strip(), inline=False)

        rules_msg = await rules_channel.send(embed=embed)
        await rules_msg.add_reaction(":white_check_mark:")
