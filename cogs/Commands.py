from utils.verification import Verification


import discord
from discord import app_commands
from discord.ext import commands

from pathlib import Path


path = str(Path(__file__).parents[0].parents[0])


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

        
    @app_commands.command(name="verification")
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def verification(self, interaction: discord.Interaction):
        embed=discord.Embed(title="Vérification", description=f"Appuyez sur le bouton correspondant à votre status.\n\n🧑‍🎓 - Eleve de l'IUT Informatique de Reims\n🧑‍🏫 - Professeur de l'IUT Informatique de Reims\n👤 - Autre / Invité\n\n**Tout abus sera sanctionné !**", color=0x5271ff)
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=self.client.footer_text, icon_url=self.client.avatar_url)
        await interaction.response.send_message(embed=embed, view=Verification())
        

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        embed=discord.Embed(title="Lovelace", description=f" **Ping**: `{round(self.client.latency * 1000)} ms`", color=0x5271ff)
        embed.set_thumbnail(url=self.client.user.avatar.url)
        embed.set_footer(text=self.client.footer_text, icon_url=self.client.avatar_url)
        await interaction.response.send_message(embed=embed)


    @commands.command(help="sync", hidden=True)
    @commands.is_owner()
    async def sync(self, ctx):
        await self.client.tree.sync()
        await ctx.send("Done")


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content == self.client.user.mention:
            embed=discord.Embed(description=f"Wesh {message.author.mention}! Oui c'est moi, Lovelace, pionnière de l'informatique je suis là pour aider le BDE BIN'HARRY !", color=0x5271ff)
            embed.set_author(name="Lovelace", icon_url=self.client.user.avatar.url)  
            embed.set_footer(text=self.client.footer_text, icon_url=self.client.avatar_url)
            try:
                await message.reply(embed=embed)
            except:
                try:
                    await message.author.send(embed=embed)
                except:
                    pass

                       
async def setup(client):
    await client.add_cog(Commands(client))
