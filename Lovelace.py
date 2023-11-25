from utils.verification import Verification


import discord
from discord.ext import commands


import logging
import json

from os import listdir
from pathlib import Path
from time import time
from datetime import datetime
from datetime import datetime


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents(
            messages = True, # for syncing purposes
            guilds = True, # to get guild channels
            voice_states = True,
            members = True,
            bans = True,
            message_content = True,
        )
        super().__init__(
            command_prefix = commands.when_mentioned_or("-"), 
            intents=intents, 
            owner_ids = [
                0, # Owner ID
            ], 
            help_command = None,
            allowed_mentions = discord.AllowedMentions(
                everyone=False, 
                users=True, 
                roles=False, 
                replied_user=True
            ),
            slash_commands = True,
            activity = discord.Activity(name=f"BIN HARRY", type=discord.ActivityType.watching),
            status = discord.Status.online
        )


        # Embed Color
        self.color = 0x2F3136
            
        # Bot Path
        self.path = str(Path(__file__).parents[0])
        

        self.footer_text = f"Lovelace • v1.0.2" 


        # Variables
        self.logs = None
        self.ready = False
        self.cache = {}

        self.launch = str(time()).split(".")[0]
        self.launch_time = datetime.utcnow()


        with open(f"{self.path}/config.json", "r") as f:
            self.config = json.load(f)

        self.persistent_views_added = False


        # Logging
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        
        handler = logging.FileHandler(f"{self.path}/logging/logs.log") # Error Handler
        handler.setLevel(logging.ERROR)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.log.addHandler(handler)
        
        handler = logging.FileHandler(f"{self.path}/logging/info.log") # Info handler
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.log.addHandler(handler)
        
    
        self.log.info("New Boot\n---------------------------------------------------------")
    
    
    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(Verification())


        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

        self.log.info('Logged in as')
        self.log.info(self.user.name)
        self.log.info(self.user.id)
        
        print(f"Lovelace is now on!\n>> {datetime.utcnow()}\n")
        self.log.info(f"Lovelace is now on!\n>> {datetime.utcnow()}\n")
        self.ready = True

        self.avatar_url = self.user.avatar.url


        # Config
        self.guild_id = self.config['GUILD_ID']    
        
        guild = self.get_guild(self.config['GUILD_ID'])

        self.verif_channel = guild.get_channel(self.config['verif']['channel'])
        self.verif_logs = guild.get_channel(self.config['verif']['logs'])

        self.verif_role = guild.get_role(self.config['verif']['role'])
        self.prof_role = guild.get_role(self.config['verif']['prof'])
        self.invite_role = guild.get_role(self.config['verif']['role'])

        self.classe = guild.get_role(self.config['verif']['classe'])
        self.activites = guild.get_role(self.config['verif']['activites'])

        self.arrivees = guild.get_role(self.config['arrivees'])
        self.departs = guild.get_role(self.config['departs'])

        self.voice = guild.get_channel(self.config['voice']['channel'])


    async def close(self):
        await self.session.close()
        await super().close()


    async def run(self):
        for file in listdir(self.path + "/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                try:
                    await self.load_extension(f"cogs.{file[:-3]}")
                    self.log.info(f"Loaded {file[:-3]} cog")
                except Exception as e:
                    self.log.error(f"Error loading {file[:-3]} cog: {e}")
