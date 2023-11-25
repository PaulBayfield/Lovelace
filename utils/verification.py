import discord


class Verification(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(emoji="🧑‍🎓", label="Elève", style=discord.ButtonStyle.blurple, row=0, custom_id="verification:eleve")
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.client.verif_role in interaction.user.roles or interaction.client.prof_role in interaction.user.roles or interaction.client.invite_role in interaction.user.roles:
            return await interaction.response.send_message(content="Tu est déjà verifié(e) !", ephemeral=True)
        else:
            return await interaction.response.send_modal(Eleve())

    @discord.ui.button(emoji="🧑‍🏫", label="Professeur", style=discord.ButtonStyle.gray, row=0, custom_id="verification:professeur")
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.client.verif_role in interaction.user.roles or interaction.client.prof_role in interaction.user.roles or interaction.client.invite_role in interaction.user.roles:
            return await interaction.response.send_message(content="Tu est déjà verifié(e) !", ephemeral=True)
        else:
            return await interaction.response.send_modal(Prof())

    @discord.ui.button(emoji="👤", label="Autre / Invité", style=discord.ButtonStyle.gray, row=0, custom_id="verification:invte")
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.client.verif_role in interaction.user.roles or interaction.client.prof_role in interaction.user.roles or interaction.client.invite_role in interaction.user.roles:
            return await interaction.response.send_message(content="Tu est déjà verifié(e) !", ephemeral=True)
        else:
            return await interaction.response.send_message(content="Merci de contacter un membre du BDE pour une vérification manuelle !", ephemeral=True)


class Eleve(discord.ui.Modal, title='Formulaire - Eleve'):
    nom = discord.ui.TextInput(
        label='Nom',
        style=discord.TextStyle.short,
        placeholder='Tapez votre nom ici...',
        required=True,
        max_length=30,
    )

    prenom = discord.ui.TextInput(
        label='Prénom',
        style=discord.TextStyle.short,
        placeholder='Tapez votre prénom ici...',
        required=True,
        max_length=30,
    )

    niveau = discord.ui.TextInput(
        label='Niveau S1/S2 - S3/S4 - S5/S6',
        style=discord.TextStyle.short,
        placeholder='Tapez votre votre niveau, example : S1',
        required=True,
        max_length=2,
    )

    classe = discord.ui.TextInput(
        label='Votre Groupe de TD',
        style=discord.TextStyle.short,
        placeholder='Tapez votre groupe de TD, example : td3',
        required=True,
        max_length=3,
    )


    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        role = None
        if self.niveau.value.lower() in ["s1", "s2", "s3", "s4", "s5"]:
            if self.classe.value.lower() in ["td1", "td2", "td3", "td4", "td5"]:
                for r in interaction.guild.roles:
                    if self.niveau.value.lower() in r.name.lower():
                        if self.classe.value.lower() in r.name.lower():
                            role = r

        if role:
            roles = [role, interaction.client.classe, interaction.client.activites, interaction.client.verif_role]
            await interaction.user.add_roles(*roles, reason=f'Verification Automatique - `{interaction.user}`', atomic=True)
            
            try:
                await interaction.user.edit(nick=f"{self.prenom.value.lower().title()} {self.nom.value.lower().title()}")
            except:
                await interaction.followup.send(content=f"Je ne peut pas te renommer (limite de Discord), renomme toi en `{self.prenom.value.lower().title()} {self.nom.value.lower().title()}`.", ephemeral=True)

            embed=discord.Embed(title=f"Vérification", description=f"Bonjour `{self.prenom.value.lower().title()} {self.nom.value.lower().title()}`, vous êtes désormais verifié !\n\n- Ajout des rôles {' '.join([r.mention for r in roles])}.", color=interaction.client.color)
            embed.set_footer(text=interaction.client.footer_text, icon_url=interaction.client.avatar_url)
            await interaction.followup.send(embed=embed, ephemeral=True)


            embed=discord.Embed(title=f"Vérification", description=f"✅ `{self.prenom.value.lower().title()} {self.nom.value.lower().title()}` - {interaction.user.mention}\n\n- Ajout des rôles {' '.join([r.mention for r in roles])}.", color=interaction.client.color)
            embed.set_footer(text=interaction.client.footer_text, icon_url=interaction.client.avatar_url)
            await interaction.client.verif_logs.send(embed=embed)
        else:
            await interaction.followup.send(content="Certaines données sont invalides...", ephemeral=True)

            embed=discord.Embed(title=f"Vérification", description=f"❌ `{self.prenom.value.lower().title()} {self.nom.value.lower().title()}` - {interaction.user.mention}\n\n- Niveau `{self.niveau.value}`\n- Groupe TD `{self.classe.value}`", color=interaction.client.color)
            embed.set_footer(text=interaction.client.footer_text, icon_url=interaction.client.avatar_url)
            await interaction.client.verif_logs.send(embed=embed)


    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        interaction.client.log.info(error)
        await interaction.followup.send('Oops! Something went wrong.', ephemeral=True)


class Prof(discord.ui.Modal, title='Formulaire - Prof'):
    nom = discord.ui.TextInput(
        label='Nom',
        style=discord.TextStyle.short,
        placeholder='Tapez votre nom ici...',
        required=True,
        max_length=30,
    )

    prenom = discord.ui.TextInput(
        label='Prénom',
        style=discord.TextStyle.short,
        placeholder='Tapez votre prénom ici...',
        required=True,
        max_length=30,
    )

    matiere = discord.ui.TextInput(
        label='Matière(s) enseignée(s)',
        style=discord.TextStyle.long,
        placeholder='Tapez vos matières ici...',
        required=True,
        max_length=200,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        roles = [interaction.client.prof_role, interaction.client.activites]

        await interaction.user.add_roles(*roles, reason=f'Verification Automatique - `{interaction.user}`', atomic=True)
        
        try:
            await interaction.user.edit(nick=f"{self.prenom.value.lower().title()} {self.nom.value.lower().title()}")
        except:
            await interaction.followup.send(content=f"Je ne peut pas te renommer (limite de Discord), renomme toi en `{self.prenom.value.lower().title()} {self.nom.value.lower().title()}`.", ephemeral=True)

        embed=discord.Embed(title=f"Vérification", description=f"Bonjour `{self.prenom.value.lower().title()} {self.nom.value.lower().title()}`, vous êtes désormais verifié !\n\n- Ajout des rôles {' '.join([r.mention for r in roles])}.", color=interaction.client.color)
        embed.set_footer(text=interaction.client.footer_text, icon_url=interaction.client.avatar_url)
        await interaction.followup.send(embed=embed, ephemeral=True)


        embed=discord.Embed(title=f"Vérification", description=f"✅ `{self.prenom.value.lower().title()} {self.nom.value.lower().title()}` - {interaction.user.mention}\n\n🧑‍🏫 Matière : `{self.matiere.value}`\n\n- Ajout des rôles {' '.join([r.mention for r in roles])}.", color=interaction.client.color)
        embed.set_footer(text=interaction.client.footer_text, icon_url=interaction.client.avatar_url)
        await interaction.client.verif_logs.send(embed=embed)


    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        interaction.client.log.info(error)
        await interaction.followup.send('Oops! Something went wrong.', ephemeral=True)
