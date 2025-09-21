from datetime import timedelta , datetime
from config import iran_offset

def is_violation(health, status, name, players):
    return health < 85 and status == "in" and name in players

def is_time_far_enough(time1, time2, minutes=2):
    if abs(time1 - time2) >= timedelta(minutes=minutes):
        return True
    else:
        return False


async def avail_fine(target_channel, name):
    now = datetime.utcnow() + iran_offset
    start_time = datetime(now.year, now.month, now.day)
    end_time = start_time + timedelta(days=1)

    async for msg in target_channel.history(after=start_time, before=end_time, oldest_first=True):
        for embed in msg.embeds:
            for field in embed.fields:
                if field.name.strip() == "پلیر" and field.value.strip() == name:
                    return True
                else:
                    return False