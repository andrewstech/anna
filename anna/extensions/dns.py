#Copyright (c) 2024 - present, MaskDuck

from __future__ import annotations

import nextcord
from dns import resolver as _dnsresolver
from nextcord.ext import commands


def construct_embed(url: str, full_answer: str):
    return nextcord.Embed(
        title=f"DNS Records for {url}",
        description=full_answer,
        color=nextcord.Color.blue(),
    )


class DNS(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self._bot: commands.Bot = bot

    @commands.command(aliases=["dns"])
    async def dig(self, ctx: commands.Context, url: str):
        """Prints DNS records for a domain."""
        record_types = ["A", "CNAME", "AAAA", "MX", "TXT", "SRV", "PTR"]
        full_answer = ""

        for record_type in record_types:
            try:
                answers = _dnsresolver.resolve(url, record_type)
                records = "\n".join([str(ans) for ans in answers])
                if records:
                    full_answer += f"**{record_type} Records**\n```{records}```\n"
            except _dnsresolver.NoAnswer:
                continue
            except _dnsresolver.NXDOMAIN:
                await ctx.send(f"Domain '{url}' does not exist.")
                return

        if full_answer:
            await ctx.send(embed=construct_embed(url, full_answer))
        else:
            await ctx.send(f"No records found for {url}.")

    @nextcord.slash_command(name="dig")
    async def dig_(
        self,
        interaction: nextcord.Interaction,
        url: str = nextcord.SlashOption(
            description="The URL to dig for DNS records. Be sure to remove http or https://", 
            required=True,
        ),
    ) -> None:
        """Dig an URL for its DNS records."""
        record_types = ["A", "CNAME", "AAAA", "MX", "TXT", "SRV", "PTR"]
        full_answer = ""

        for record_type in record_types:
            try:
                answers = _dnsresolver.resolve(url, record_type)
                records = "\n".join([str(ans) for ans in answers])
                if records:
                    full_answer += f"**{record_type} Records**\n```{records}```\n"
            except _dnsresolver.NoAnswer:
                continue
            except _dnsresolver.NXDOMAIN:
                await interaction.send(f"Domain '{url}' does not exist.")
                return

        if full_answer:
            await interaction.send(embed=construct_embed(url, full_answer))
        else:
            await interaction.send(f"No records found for {url}.")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(DNS(bot))