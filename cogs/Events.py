import discord
from discord import app_commands
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == self.client.guild_id and self.client.arrivees:
            embed=discord.Embed(description=f"Bienvenu(e) {member.mention} sur le serveur du BDE Informatique BIN'HARRY !", color=self.client.color)
            embed.add_field(name="\u2063", value=f"*Membre **`#{sorted(member.guild.members, key=lambda m: m.joined_at).index(member)+1}`***")
            embed.set_author(name=member.name, icon_url=member.display_avatar.url)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=self.client.footer_text, icon_url=self.client.avatar_url)
            await self.client.arrivees.send(embed=embed, content=member.mention)


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.client.guild_id and self.client.departs:
            embed=discord.Embed(description=f"Aurevoir {member}...", color=self.client.color)
            embed.set_author(name=member.name, icon_url=member.display_avatar.url)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=self.client.footer_text, icon_url=self.client.avatar_url)
            await self.client.departs.send(embed=embed, content=member.mention)


async def setup(client):
    await client.add_cog(Events(client))