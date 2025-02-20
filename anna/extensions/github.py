from __future__ import annotations
import re
from typing import List
import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View

# GitHub request helper
async def request(*args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(*args, **kwargs) as ans:
            return await ans.json()

# Regex patterns
FULL_MATCH_ANY_REPO = r"(https:\/\/github.com\/)?([A-Za-z1-9-]+)\/([A-Za-z1-9-]+)(\/pull)?(#|\/)(?P<pr_id>\d+)"
VERY_SHORT_MESSAGE = r"##(\d+)"
PR_CHANNEL_ID = 1130858271620726784
STAFF_ROLE_ID = 1197475623745110109

# PR_CHANNEL_ID = 1281898370134183950
# STAFF_ROLE_ID = 1281898369245253741

class _PRRawObject(object):
    def __init__(self, *, repo_owner: str, repo_name: str, pr_id: str) -> None:
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.pr_id = pr_id

class GitHub(commands.Cog):
    """This module sends embeds when a user links a Github repository/PR/issue. For repositories, use repo:example/example. For PRs/issues, example/example#number. \nFor is-a-dev/register PRs/issues, use ##PR_NUMBER."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def fetch_pr_status(self, pr: _PRRawObject) -> nextcord.Embed:
        try:
            # Fetch PR/issue information from GitHub
            i = await request("GET", f"https://api.github.com/repos/{pr.repo_owner}/{pr.repo_name}/issues/{pr.pr_id}",)
            
            if i.get('pull_request', {}).get('merged_at'):
                color = nextcord.Color.purple() 
                merger = i.get('closed_by', {}).get('login')
                status = "Merged by " + merger
            elif i.get('state') == "closed":
                color = nextcord.Color.red()
                closer = i.get('closed_by', {}).get('login')
                status = "Closed by " + closer
            else:
                color = nextcord.Color.green()
                status = "Open"

            embed = nextcord.Embed(
                title=f"PR/Issue: {pr.repo_owner}/{pr.repo_name}",
                description=f"[(#{pr.pr_id}) {i['title']}]({i['html_url']})",
                color=color,
            )
            embed.add_field(name="Status", value=status, inline=True)

            return embed
        except aiohttp.ClientError as e:
            embed = nextcord.Embed(
                title="Error",
                description=f"Error fetching PR #{pr.pr_id}: {str(e)}",
                color=nextcord.Color.red(),
            )
            return embed

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return

        # Match for repo format 'repo:owner/repo'
        repo_matches: List[re.Match] = re.findall(r"repo:([A-Za-z1-9-]+)/([A-Za-z1-9-]+)", message.content)
        full_matches: List[re.Match] = re.findall(FULL_MATCH_ANY_REPO, message.content)
        very_short_matches: List[re.Match] = re.findall(VERY_SHORT_MESSAGE, message.content)

        pr_list: List[_PRRawObject] = []

        # Handle PRs/issues from full matches (links or #)
        if len(full_matches) > 0:
            for x in full_matches:
                if x[0] == "https://github.com/":
                    await message.edit(suppress=True)
                repo_owner = x[1]
                repo_name = x[2]
                pr_id = x[5]
                pr_list.append(_PRRawObject(repo_owner=repo_owner, repo_name=repo_name, pr_id=pr_id))

        # Handle very short messages (##PRNUMBER)
        if len(very_short_matches) > 0:
            for pr_id in very_short_matches:
                pr_list.append(_PRRawObject(repo_owner="is-a-dev", repo_name="register", pr_id=pr_id))

        # Only process PR/issue embed once for all PRs/issues
        if len(pr_list) > 0:
            for pr in pr_list:
                embed = await self.fetch_pr_status(pr)

                # Button for refreshing the PR status
                refresh_button = Button(label="Refresh Status", style=nextcord.ButtonStyle.primary)

                async def refresh_callback(interaction: nextcord.Interaction):
                    new_embed = await self.fetch_pr_status(pr)
                    await interaction.response.edit_message(embed=new_embed)

                refresh_button.callback = refresh_callback
                view = View(timeout=None)
                view.add_item(refresh_button)
                await message.channel.send(embed=embed, view=view)
            
            return  # Prevent sending another embed below
        
        # Handle repo:owner/repo matches
        if len(repo_matches) > 0:
            for repo_owner, repo_name in repo_matches:
                try:
                    repo_info = await request("GET", f"https://api.github.com/repos/{repo_owner}/{repo_name}")
                    owner_info = await request("GET", f"https://api.github.com/users/{repo_owner}")
                    owner_name = owner_info.get("login", "Unknown")
                    owner_avatar = owner_info.get("avatar_url", "")
                    repo_url = repo_info.get("html_url", f"https://github.com/{repo_owner}/{repo_name}")
                    repo_description = repo_info.get("description", "No description available")
                    stars = repo_info.get("stargazers_count", 0)
                    forks = repo_info.get("forks_count", 0)
                    repo_banner = repo_info.get("social_preview_url", "")

                    embed = nextcord.Embed(
                        title=f"Repository: {repo_owner}/{repo_name}",
                        description=f"[Visit Repository]({repo_url})\n{repo_description}",
                        color=nextcord.Color.blue(),
                    )
                    embed.set_thumbnail(url=owner_avatar)
                    embed.add_field(name="Stars", value=str(stars), inline=True)
                    embed.add_field(name="Forks", value=str(forks), inline=True)

                    if repo_banner:
                        embed.set_image(url=repo_banner)

                    await message.channel.send(embed=embed)
                except aiohttp.ClientError as e:
                    await message.channel.send(f"Error fetching repository {repo_owner}/{repo_name}: {str(e)}")
                    continue
        if len(pr_list) == 0:
            if message.channel.id == PR_CHANNEL_ID:
                if message.author.get_role(STAFF_ROLE_ID) is None:  # type: ignore
                    await message.delete()

            return

def setup(bot: commands.Bot) -> None:
    bot.add_cog(GitHub(bot))
