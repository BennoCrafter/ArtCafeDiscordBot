import asyncio
import os

import interactions
from interactions.models import OptionType

from src import logutil

logger = logutil.init_logger(os.path.basename(__file__))

DM_TIMEOUT = 10  # seconds per DM attempt
DM_DELAY = 0.5  # seconds between users


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

        sent = 0
        failed = 0
        timed_out = 0
        txt = """**ART CAFE – DIE CHALLENGE STARTET! :coffee::art:**

        Hey! Lange war der Server inaktiv und ist schon ausgestorben, doch wir wollen ihm eine neue Chance geben. Seid dabei und lasst uns den einst so farbenfrohen Server wieder etwas Farbe schenken :) Ladet gerne eure Freunde ein! Euch werden verschiedene Minigames und Challenges erwarten.

        Und deshalb starten wir auch direkt mit einer kleinen Challenge:
        Das Thema für den Monat September ist "Portrait". Also malt ein paar Gesichter! Es ist eine super Übung, um Proportionen, Licht und Schatten zu lernen. Ihr könnt ein längeres Gemälde malen oder auch nur eine kleine Skizze anfertigen. Macht gerne mit und habt an oberster Stelle stehend Spaß. Falls ihr noch ein paar Tipps braucht oder Fragen habt, dann meldet euch hier!

        :art: Egal, ob ihr zeichnet, malt, designt, fotografiert oder einfach generell ein Auge für Kunst habt – jede Art von Kunst und jeder hier ist herzlich willkommen! :sparkles:

        Seid ihr dabei? Dann lasst uns gemeinsam den Server wieder aufleben lassen! Und sorry für den Ping :("""

        for member in ctx.guild.members:
            if member.bot:
                continue

            # Use the role selected in /send_dm
            if not any(str(role.id) == role_id for role in member.roles):
                continue

            try:
                await asyncio.wait_for(
                    member.user.send(txt),
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

        await ctx.send(
            f"✅ Sent: `{sent}`\n❌ Failed: `{failed}`\n⏱️ Timed out: `{timed_out}`",
            ephemeral=True,
        )
