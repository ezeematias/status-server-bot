import discord
from discord.ext import commands, tasks
from rcon.source import Client
import socket
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PASSWORD = os.getenv('RCON_PASSWORD')
HOST = os.getenv('HOST_DNS')

servers = {
    "The Island": {"port": 32330},
    "Ragnarok": {"port": 32331},
    "Valguero": {"port": 32332},
    "The Center": {"port": 32333},
    "Extinction": {"port": 32334},
    "Aberration": {"port": 32335},
    "Crystal Isles": {"port": 32336},
    "Lost Island": {"port": 32337},
    "Scorched Earth": {"port": 32338},
    "Fjordur": {"port": 32339},
    "Genesis 1": {"port": 32340},
    "Genesis 2": {"port": 32341},
    "Astral": {"port": 32342},
    "VIP Hope": {"port": 32343}
}

intents = discord.Intents.default()
intents.presences = False
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

async def get_server_status(server_name, host, port, password):
    try:
        with Client(host, port, passwd=password) as client:
            response = client.run('ListPlayers')
            return response is not None
    except (socket.timeout, ConnectionRefusedError, socket.gaierror):
        return False
    except Exception as e:
        print(f"Error al conectar con el servidor {server_name} mediante RCON: {e}")
        return False

async def update_channel_names():
    existing_channels = {channel.name: channel for channel in bot.get_all_channels()}

    for server_name, server_data in servers.items():
        host = HOST
        port = server_data["port"]
        password = PASSWORD
        status = await get_server_status(server_name, host, port, password)       

        status_emoji = "🟢" if status else "🔴"

        channel = next((ch for ch in existing_channels.values() if ch.name.startswith(server_name)), None)

        if channel:
            new_name = f"{server_name} {status_emoji}"            

            if channel.name != new_name:
                print(f"{channel.name} actualizando a {new_name}.")
                await channel.edit(name=new_name)
            else:
                print(f"{channel.name} ya está actualizado.")
        else:
            print(f"No se encontró el canal para '{server_name}'.")

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} ha iniciado sesión.')
    update_status.start()

@tasks.loop(minutes=3)
async def update_status():
    await update_channel_names()

bot.run(TOKEN)
