import os

import interactions

from src import logutil
from src.load_gifs import get_gif_urls
from pathlib import Path
import random


logger = logutil.init_logger(os.path.basename(__file__))

gifs_urls = get_gif_urls(Path("resources/gif_urls.json"))

category_emoji = {
    "cuddle": "🤗",
    "hug": "🫂",
    "kiss": "💋",
    "pat": "🤚",
    "poke": "👉",
    "highfive": "🙌",
    "bonk": "🔨",
    "slap": "👋💥",
    "wave": "👋"
}

action_verbs = {
    "cuddle": "cuddles",
    "hug": "hugs",
    "kiss": "kisses",
    "pat": "pats",
    "poke": "pokes",
    "highfive": "high fives",
    "bonk": "bonks",
    "slap": "slaps",
    "wave": "waves at"
}


class Rolelplay(interactions.Extension):
    @interactions.slash_command(
        "roleplay", description="base roleplay command"
    )
    async def roleplay(self, ctx: interactions.SlashContext):
        ...

    @roleplay.subcommand(
        "hug", sub_cmd_description="Hug someone"
    )
    @interactions.slash_option(
        "user",
        "The user to hug",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def hug(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "hug", user)

    @roleplay.subcommand(
        "cuddle", sub_cmd_description="Cuddle someone"
    )
    @interactions.slash_option(
        "user",
        "The user to cuddle",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def cuddle(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "cuddle", user)

    @roleplay.subcommand(
        "kiss", sub_cmd_description="Kiss someone"
    )
    @interactions.slash_option(
        "user",
        "The user to kiss",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def kiss(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "kiss", user)

    @roleplay.subcommand(
        "pat", sub_cmd_description="Pat someone"
    )
    @interactions.slash_option(
        "user",
        "The user to pat",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def pat(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "pat", user)

    @roleplay.subcommand(
        "poke", sub_cmd_description="Poke someone"
    )
    @interactions.slash_option(
        "user",
        "The user to poke",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def poke(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "poke", user)

    @roleplay.subcommand(
        "highfive", sub_cmd_description="High five someone"
    )
    @interactions.slash_option(
        "user",
        "The user to high five",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def highfive(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "highfive", user)

    @roleplay.subcommand(
        "slap", sub_cmd_description="Slap someone"
    )
    @interactions.slash_option(
        "user",
        "The user to slap",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def slap(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "slap", user)

    @roleplay.subcommand(
        "wave", sub_cmd_description="Wave at someone"
    )
    @interactions.slash_option(
        "user",
        "The user to wave at",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def wave(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "wave", user)

    @roleplay.subcommand(
        "bonk", sub_cmd_description="Bonk someone"
    )
    @interactions.slash_option(
        "user",
        "The user to bonk",
        opt_type=interactions.OptionType.MENTIONABLE,
        required=False,
    )
    async def bonk(self, ctx: interactions.SlashContext, user: interactions.User | None = None):
        await self.send_roleplay(ctx, "bonk", user, image_url="https://media1.tenor.com/m/_ZvbLvrT_QcAAAAd/horny-jail-bonk.gif")


    async def send_roleplay(self, ctx: interactions.SlashContext, action: str, user: interactions.User | None = None, image_url: Path | str | None = None):
        if user is None:
            msg = f"{ctx.author.mention} {action}!"
        else:
            msg = f"{ctx.author.mention} {action_verbs.get(action, action)} {user.mention}!"

        e: interactions.Embed = interactions.Embed(
            title=f"{category_emoji.get(action, "°")} {action.capitalize()}!",
            description=msg,
            color=interactions.Color.random(),
        )
        if image_url is None:
            e.set_image(url=random.choice(gifs_urls.get(action, [])))
        elif isinstance(image_url, Path):
            image_url = image_url.resolve().as_posix()
        else:
            e.set_image(url=image_url)

        await ctx.send(embed=e)
