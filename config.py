import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))
ROLE_ID = 1
STATS_CHANNEL_ID = 1

players = {
    
}

whitelist = {
    

}

admins = {
    
}

ignore = {
    
}

iran_offset = timedelta(hours=3, minutes=30)