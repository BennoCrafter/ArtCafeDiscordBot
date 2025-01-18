import requests
import os
from dotenv import load_dotenv

load_dotenv()

valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._?'

TOKEN = os.getenv('TOKEN')
GUILD_ID = '1315565007618048020'

def urify(string: str) -> str:
    r = "".join([char if char in valid_chars else "" for char in string])
    return "???" if r == "" else r

def get_guild_channels():
    headers = {
        'Authorization': f'Bot {TOKEN}',
    }

    url = f'https://discord.com/api/v10/guilds/{GUILD_ID}/channels'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        channels = response.json()
        for channel in channels:
            print(f"Channel ID: {channel['id']}")
            print(f"Channel Name: {channel['name']} || {urify(channel['name'])}")
            print(f"Channel Type: {channel['type']}")
            print("---")
    else:
        print(f"Error: {response.status_code}")

get_guild_channels()
