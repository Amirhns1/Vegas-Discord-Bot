import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import asyncio


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = 895225877003112478
SOURCE_CHANNEL_ID = 1416647211646976020
TARGET_CHANNEL_ID = 1416653108997652531
ADMIN_USER_ID = 739010795010261032
players = {
    "Ali_Wallhack": 614109280508968980,
    "Hasan_Soniapoor": 411916947773587456,
    "Parsa_Erx" : 547905866255433758,
    "Jack_Davis" : 739010795010261032
}
iran_offset = timedelta(hours=3, minutes=30)

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.dm_messages = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # سینک کردن کامندها فقط برای یک گیلد (سرور)
        self.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))


client = MyClient()
async def process_message(message: discord.Message, target_channel: discord.TextChannel):
    content = message.content.splitlines()

    health_value = None
    player_name = None
    plate_number = None

    for line in content:
        if line.startswith("Health"):
            try:
                health_value = int(line.split(":")[1].strip().replace("%", ""))
            except:
                pass
        if line.startswith("Plate"):
            plate_number = line.split(":")[1].strip()
        if line.startswith("steam:"):
            parts = line.split()
            if len(parts) >= 2:
                player_name = parts[1].strip()

    if health_value is not None and player_name and plate_number:
        if health_value < 85 and player_name in players:
            local_time = message.created_at + iran_offset
            time_str = local_time.strftime("%H:%M")
            user_id = players[player_name]

            embed = discord.Embed(
                title=f"🚨 وضعیت سلامت پایین",
                color=discord.Color.dark_purple(),
                timestamp=local_time
            )
            embed.add_field(name="پلیر", value=f"{player_name}", inline=False)
            embed.add_field(name="سلامت موتور", value=f"{health_value}%", inline=False)
            embed.add_field(name="پلاک", value=plate_number, inline=False)
            embed.add_field(name="زمان وقوع", value=time_str, inline=False)

            await target_channel.send(embed=embed)
            await target_channel.send(
                f"**شما به علت گذاشتن این ماشین زیر 85% مبلغ 45K جریمه شدید.**\n"
                f"*برای پرداخت به شماره کارت **267-584** واریز و اسکرین شات رو برای ربات ارسال کنید.*\n"
                f"<@{user_id}>"
            )
            await asyncio.sleep(2)


@client.tree.command(name="check", description="بررسی پیام‌ها برای today یا yesterday")
@app_commands.describe(input="مثلاً today یا yesterday")
async def check_command(interaction: discord.Interaction, input: str):
    input = input.replace(" ", "").lower()

    if input not in ["today", "yesterday"]:
        await interaction.response.send_message("ورودی باید today یا yesterday باشه.", ephemeral=True)
        return
    now = datetime.utcnow() + iran_offset
    if input == "today":
        start_time = datetime(now.year, now.month, now.day)
    else:
        start_time = datetime(now.year, now.month, now.day) - timedelta(days=1)

    end_time = start_time + timedelta(days=1)

    source_channel = client.get_channel(SOURCE_CHANNEL_ID)
    target_channel = client.get_channel(TARGET_CHANNEL_ID)

    count = 0
    async for message in source_channel.history(after=start_time, before=end_time, oldest_first=True):
        await process_message(message, target_channel)
        count += 1

    await interaction.response.send_message(
        f"Done!",
        ephemeral=True
    )
@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    if message.channel.id == SOURCE_CHANNEL_ID:
        target_channel = client.get_channel(TARGET_CHANNEL_ID)
        if target_channel is None:
            target_channel = await client.fetch_channel(TARGET_CHANNEL_ID)
        
        await process_message(message, target_channel)
        await asyncio.sleep(2)
        

    # جلوگیری از حلقه بی‌پایان
    if message.author == client.user:
        return

    # فقط پیام‌های DM
    if isinstance(message.channel, discord.DMChannel):
        if message.attachments:
            admin_user = await client.fetch_user(ADMIN_USER_ID)
            for attachment in message.attachments:
                username = next((name for name, pid in players.items() if pid == message.author.id), None)
                if username in players:
                    await admin_user.send(
                        content=f"📸 From {username}",
                        file=await attachment.to_file()
                    )
                else:
                    await message.channel.send("شما پلیر وگاس نیستید!")

        else:
            await message.channel.send("لطفاً یک تصویر ارسال کنید.")

client.run(TOKEN)