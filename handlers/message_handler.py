import discord
from config import players, iran_offset, ADMIN_USER_ID, whitelist , ignore
from utils.extract_info import extract_message_info
from utils.violation_check import is_violation, is_time_far_enough, avail_fine

async def process_message(message: discord.Message, target_channel: discord.TextChannel, source_channel: discord.TextChannel):
    health, name, plate, status = extract_message_info(message)
    if name in ignore:
        return
    result = await avail_fine(target_channel, name)
    if not is_violation(health, status, name, players):
        return

    local_time = message.created_at + iran_offset
    time_str = local_time.strftime("%H:%M")
    checked = False

    async for msg in source_channel.history(limit=50, before=message.created_at, oldest_first=False):
        content = msg.content.splitlines()
        plate2 = None
        if any(line.startswith("Bardasht") for line in content):
            for line in content:
                if line.startswith("steam:"):
                    parts = line.split()
                    if len(parts) >= 2:
                        player_name = parts[1].strip()
                if line.startswith("Plate"):
                    plate2 = line.split(":")[1].strip()
            user_id = players[player_name]
        if not checked:
            if plate2 == plate and player_name == name:
                time_2 = msg.created_at + iran_offset
                if is_time_far_enough(local_time, time_2) and not result:
                    embed = discord.Embed(
                        title="🚨 وضعیت سلامت پایین",
                        color=discord.Color.red(),
                    )
                    embed.add_field(name="پلیر", value=name, inline=False)
                    embed.add_field(name="سلامت موتور", value=f"{health}%", inline=False)
                    embed.add_field(name="پلاک", value=plate, inline=False)
                    embed.add_field(name="زمان وقوع", value=time_str, inline=False)

                    await target_channel.send(embed=embed)
                    if name in ignore:
                        return
                    if name in whitelist:
                        temp = 15
                    else:
                        temp = 45
                    await target_channel.send(
                        f"**شما به علت گذاشتن این ماشین زیر 85% مبلغ {temp}K جریمه شدید.**\n"
                        f"*برای پرداخت تا 24 ساعت مهلت دارید به شماره کارت **260-467** واریز و اسکرین شات رو برای ربات ارسال کنید.*\n"
                        f"<@{user_id}>"
                    )
                    await target_channel.send("`------------------------------`")
                    break
                else:
                    checked = True
        else:
            break