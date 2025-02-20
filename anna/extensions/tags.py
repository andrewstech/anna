"""
Copyright (c) 2024 - present, MaskDuck

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
# ruff: noqa
import nextcord
from nextcord.ext import commands

nohelp = """
This is not a help channel!\n
We have a help channel for a reason, see <#1228996111390343229>.\n
Please use that for help. Open a thread, even if it is a tiny problem.\n
So... **Enjoy troll answers past this message and take them with a pinch of salt. The action of following any help in this channel past this message is at your own risk. You've been warned.**\n
Please read the [is-a.dev docs](https://www.is-a.dev/docs/)\n
Have fun!"""

waittime = """
Us maintainers have a life; we aren't obligated to merge your PRs the moment you make your PR.\n
We have other things to do. This project is run by volunteers, so please have patience with us.\n
Instead of pinging us, send a PR in <#1130858271620726784> *once* and wait for us to review it.
"""

rtfm = """
Please read the documentation. It exists for a reason.\n
Our maintainers and helpers are volunteers. It's not our job to answer questions already answered in the documentation or FAQ.\n
- [is-a.dev documentation](https://is-a.dev/docs)
- <#991779321758896258>\n
"""
domservice = """
is-a.dev can give you support with your ***domain***, and on the condition that you've read the [documentation](https://is-a.dev/docs).\n
We do __not__ provide support for anything else. We aren't an HTML boot camp, and it's not our job to teach you JSON. We also don't provide support for Github or DNS questions either.
"""


class Tags(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def nohelp(self, ctx):
        if not ctx.channel.id in [1155589227728339074]:
            embed = nextcord.Embed(
                title="This is not a help channel.",
                description=nohelp,
                color=nextcord.Colour.blue(),
            )
            await ctx.send(embed=embed)
        else:
            msg = await ctx.send("This command cannot be used in this channel, because this is a help channel.")
            await msg.delete()

    @commands.command()
    async def waittime(self, ctx):
        if True:
            embed = nextcord.Embed(
                title="How long is it until my PR is merged?",
                description=waittime,
                color=nextcord.Colour.blue(),
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def rtfm(self, ctx):
        if True:
            embed = nextcord.Embed(
                title="Read The Fucking Manual",
                description=rtfm,
                color=nextcord.Colour.blue(),
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def domservice(self, ctx):
        if True:
            embed = nextcord.Embed(
                title="We're a domain service, and we only provide support for domains",
                description=domservice,
                color=nextcord.Colour.blue(),
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Tags(bot))
