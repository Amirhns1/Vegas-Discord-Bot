from discord import app_commands
import discord
from datetime import datetime, timedelta
from config import SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID, iran_offset ,admins  ,ROLE_ID, STATS_CHANNEL_ID
from handlers.message_handler import process_message
from datetime import timezone
from typing import Literal

class StatsButtonView(discord.ui.View):
    def __init__(self, rob, color1, temp):
        super().__init__(timeout=None)
        self.rob = rob
        self.color1 = color1
        self.temp = temp

    @discord.ui.button(label="📬 Send Stats", style=discord.ButtonStyle.secondary, custom_id="send_stats_button")
    async def send_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        stats_channel = interaction.client.get_channel(STATS_CHANNEL_ID)
        embed = discord.Embed(
            title="Vegas Robbery Stats",
            color=self.color1,
        )
        embed.add_field(name="Rob" ,value=f"{self.rob}", inline=True)
        embed.add_field(name="status" ,value=f"{self.temp}", inline=True)
        if interaction.user.id not in admins.values():
            await interaction.response.send_message("Shoma Perm Estefade az bot ro nadarid.", ephemeral=True)
            return
        await stats_channel.send(embed=embed)
        await interaction.response.send_message("Done", ephemeral=True)



def register_commands(client):
    @client.tree.command(name="check", description="بررسی پیام‌ها برای today یا yesterday")
    @app_commands.describe(input="مثلاً today یا yesterday")
    async def check_command(interaction, input: str):
        if interaction.user.id not in admins.values():
            await interaction.response.send_message("Shoma Perm Estefade az bot ro nadarid.", ephemeral=True)
            return
        input = input.replace(" ", "").lower()
        if input not in ["today", "yesterday"]:
            await interaction.response.send_message("ورودی باید today یا yesterday باشه.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        #now = datetime.utcnow() + iran_offset
        #start_time = datetime(now.year, now.month, now.day) +  timedelta(minutes=1)
        #if input == "yesterday":
        #    start_time -= timedelta(hours=48)
        #end_time = start_time + timedelta(hours=23 , minutes=58)
        now = datetime.utcnow().replace(tzinfo=timezone.utc) + iran_offset
        base = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if input == "yesterday":
            start_time = base - timedelta(days=1)
        else:
            start_time = base
        end_time = start_time + timedelta(hours=24)

        start_time_utc = (start_time - iran_offset).replace(tzinfo=timezone.utc)
        end_time_utc = (end_time - iran_offset).replace(tzinfo=timezone.utc)

        source_channel = client.get_channel(SOURCE_CHANNEL_ID)
        target_channel = client.get_channel(TARGET_CHANNEL_ID)

        count = 0
        async for msg in source_channel.history(after=start_time_utc, before=end_time_utc, oldest_first=True):
            await process_message(msg, target_channel, source_channel)
            count += 1

        await interaction.followup.send(f"Done! {count}", ephemeral=True)


    @client.tree.command(name="message", description="ارسال پیام توسط ربات")
    async def message_command(interaction, text:str):
        if interaction.user.id not in admins.values():
            await interaction.response.send_message("Shoma Perm Estefade az bot ro nadarid.", ephemeral=True)
            return
        await interaction.channel.send(text)
        await interaction.response.send_message("Done", ephemeral=True)

    @client.tree.command(name="leftcar", description="Abandoned Cars")
    async def leftcar_command(interaction, user: discord.User, ic_name:str, plate:str, time:str, fee:str ):
        if interaction.user.id not in admins.values():
            await interaction.response.send_message("Shoma Perm Estefade az bot ro nadarid.", ephemeral=True)
            return
        embed = discord.Embed(
            title="⚠️ ماشین رها شده ⚠️",
            color=discord.Color.orange(),
        )
        embed.add_field(name="پلیر", value=ic_name, inline=False)
        embed.add_field(name="پلاک", value=plate, inline=False)
        embed.add_field(name="زمان وقوع", value=time, inline=False)
        await interaction.channel.send(embed=embed)
        await interaction.channel.send(
                        f"**به علت رها کردن وسیله نقلیه مبلغ {fee}K جریمه شدید**\n"
                        f"*برای پرداخت تا 24 ساعت مهلت دارید به شماره کارت **260-467** واریز و اسکرین شات رو برای ربات ارسال کنید.*\n"
                        f"{user.mention}"
                    )


        await interaction.response.send_message("Done", ephemeral=True)


    @client.tree.command(name="op", description="Rob history")
    async def group(
        interaction, commander:discord.User,
        rob: Literal["Maze", "City", "Paleto", "GunShop", "Shams", "Flat", "Airport", "Bimeh"],
        status: Literal["Win", "Lose"],
        mvp:discord.User = None,
        robber1: discord.User = None,
        robber2: discord.User = None,
        robber3: discord.User = None,
        robber4: discord.User = None,
        robber5: discord.User = None,
        robber6: discord.User = None
        ):
        if interaction.channel != client.get_channel(1):
            await interaction.response.send_message("Dar in channel nemitavanid estefade konid!", ephemeral=True)
            return
        if not any(r.id == ROLE_ID for r in interaction.user.roles):
            await interaction.response.send_message("Shoma Role Estefade az bot ro nadarid.", ephemeral=True)
            return
        users = [u for u in [robber1, robber2, robber3, robber4, robber5, robber6] if u]
        mentions = ", ".join(u.mention for u in users)
        temp = None
        color1 = None
        if status == "Win" :
            temp = "Winner! ✅"
            color1 = discord.Color.green()
        else:
            temp = "Loser! ❌"
            color1 = discord.Color.red()

        embed = discord.Embed(
            title="Vegas Robbery Stats",
            color=color1,
        )
        embed.add_field(name="Rob" ,value=f"{rob}", inline=True)
        embed.add_field(name="Commander" ,value=f"{commander.mention}", inline=True)
        if status == "Win":
            embed.add_field(name="MVP" ,value=f"{mvp.mention}", inline=True)
        embed.add_field(name="Robbers" ,value=f"{mentions}", inline=False)
        embed.add_field(name="Stats" ,value=f"{temp}", inline=False)


        
        view = StatsButtonView(rob, color1, temp)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Done", ephemeral=True)
