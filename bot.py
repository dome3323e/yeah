import discord
import requests
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COOKIE = os.getenv("ROBLOSECURITY")
GROUP_ID = os.getenv("GROUP_ID")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

headers = {
    "Cookie": f".ROBLOSECURITY={COOKIE}",
    "User-Agent": "RobloxBot/1.0",
    "Content-Type": "application/json"
}

last_funds = None

def get_group_funds(group_id):
    url = f"https://groups.roblox.com/v1/groups/{group_id}/funds"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("funds")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

@client.event
async def on_ready():
    global last_funds
    print(f"Bot logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    while True:
        funds = get_group_funds(GROUP_ID)
        if funds is not None:
            if last_funds is None:
                last_funds = funds
                await channel.send(f"@everyone 🔍 Initial funds recorded: {funds} Robux.")
            elif funds > last_funds:
                await channel.send(f"@everyone 💸 Group funds increased! {last_funds} → {funds} Robux.")
                last_funds = funds
            else:
                print(f"No change: {funds} Robux")
        await asyncio.sleep(60)

from keep_alive import keep_alive
keep_alive()

client.run(DISCORD_TOKEN)

