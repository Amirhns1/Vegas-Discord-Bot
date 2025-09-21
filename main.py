import discord
import re
from discord.ext import commands
from config import TOKEN, GUILD_ID, ADMIN_USER_ID, players , SOURCE_CHANNEL_ID
from config import SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID, iran_offset ,admins
from handlers.command_handler import register_commands



class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.dm_messages = True
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        register_commands(self) 
        self.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))
        

client = MyClient()
source_channel = client.get_channel(SOURCE_CHANNEL_ID)
target_channel = client.get_channel(TARGET_CHANNEL_ID)
IMAGE_URL_REGEX = re.compile(r"^(https?://\S+\.(?:png|jpg|jpeg|gif|webp))$", re.IGNORECASE)

@client.event
async def on_message(message):
    if message.author.bot or message.author == client.user:
        return
    
    if isinstance(message.channel, discord.DMChannel):
        if message.content:
            match = IMAGE_URL_REGEX.match(message.content.strip())
            admin_user = await client.fetch_user(ADMIN_USER_ID)
            username = next((name for name, pid in players.items() if pid == message.author.id), None)
            if match:
                if username:
                    await admin_user.send(f"jarime az taraf: {username}\n{match.group(1)}")
                else:
                    await message.channel.send("شما پلیر وگاس نیستید!")
        else:
            await message.channel.send("فرمت اشتباه است.\nفقط لینک مستقیم عکس (jpg/png/gif/webp) مجازه 🚫")

client.run(TOKEN)