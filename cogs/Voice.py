import discord
from discord.ext import commands


import textwrap


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name.startswith("➕・")==True and after.name.startswith("➕・")==False:
            await after.edit(name=f"➕・{textwrap.shorten(after.name, width=98, placeholder='')}")
        
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel!=None:
            if before.channel.name.startswith("➕・") and len(before.channel.members)==0:
                await before.channel.delete()

                #try:
                #    await member.send(f"Ciao {member.mention}!\nLe salon temporaire `{before.channel.name}`, est désormais supprimé !")
                #except:
                #    pass

            if len(before.channel.members) == 1:
                overwrite = before.channel.overwrites_for(before.channel.members[0])
                if overwrite.move_members == True:
                    pass
                else:
                    await before.channel.set_permissions(
                        before.channel.members[0],
                        connect=True,
                        #manage_channels=True,
                        move_members=True,
                        priority_speaker=True,
                        speak=True,
                        stream=True,
                        use_voice_activation=True
                    )

                    #try:
                    #    await before.channel.members[0].send(f"Wesh {before.channel.members[0].mention}!\nTu est tout seul dans `{before.channel.name}` :'(\nTu as désormais les permissions de kick des gens de ce salon vocal.")
                    #except:
                    #    pass

        if after.channel==None:
            return

        if after.channel.id == self.client.config['voice']['channel']:
            channel = self.client.voice

            if member.nick==None:
                user=member.name
            else:
                user=member.nick    
            
            default_name = f"➕・{user}"
            overwrites = {
                after.channel.guild: discord.PermissionOverwrite(connect=False)
            }

            c = await channel.category.create_voice_channel(default_name, overwrites=overwrites, position=int(channel.position)+1)
            await c.set_permissions(
                member,
                connect=True,
                #manage_channels=True,
                move_members=True,
                priority_speaker=True,
                speak=True,
                stream=True,
                use_voice_activation=True
            )
            
            try:
                await member.move_to(c)
            except:
                await c.delete()

            #try:
            #    await member.send(f"Bonjour {member.mention}!\nTu viens de créer un salon vocal temporaire, `{after.channel.name}` qui sera supprimé lorsqu'il deviendra vide. Tu as les permissions de kick des gens de ce salon vocal.")
            #except:
            #    pass


async def setup(client):
    await client.add_cog(Voice(client))