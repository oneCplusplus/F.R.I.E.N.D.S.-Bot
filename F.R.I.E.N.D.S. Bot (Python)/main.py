import discord
from discord.ext import commands, tasks
import socket
import os

# Função para verificar o status do servidor
def check_server(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=5):
            return True
    except Exception:
        return False

# Carregar variáveis de ambiente
TOKEN = os.getenv('TOKEN', 'MTI2MzcwNTUyNTE1MDAyNzc4OA.G996cI.CyKW5m60hXZCM_b0f9uxw0JS7pHPme2nI8GahI')
GUILD_ID = int(os.getenv('GUILD_ID', '1037902632523681812'))
SERVER_IP = '26.42.12.232'
SERVER_PORT = 25565

if not TOKEN or not GUILD_ID:
    print('TOKEN or GUILD_ID is missing in environment variables.')
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print("Bot is ready!")
    await update_commands()
    update_status.start()  # Iniciar a tarefa de atualização de status

async def update_commands():
    guild = discord.Object(id=GUILD_ID)
    try:
        # Atualizar os comandos de aplicação na guilda
        await client.tree.sync(guild=guild)
        print('Successfully reloaded application (/) commands.')
    except Exception as e:
        print(f'Failed to reload application commands: {e}')

@tasks.loop(seconds=5)
async def update_status():
    is_open = check_server(SERVER_IP, SERVER_PORT)
    if is_open:
        status_message = f'Servidor aberto em {SERVER_IP}:{SERVER_PORT}'
    else:
        status_message = 'Servidor fechado ou inacessível'
    activity = discord.Game(name=status_message)
    await client.change_presence(activity=activity)

@client.tree.command(name='server', description='Check the status of the Minecraft server')
async def server(interaction: discord.Interaction):
    is_open = check_server(SERVER_IP, SERVER_PORT)
    if is_open:
        status_message = f'O servidor está aberto em **{SERVER_IP}** e `porta {SERVER_PORT}`.'
    else:
        status_message = 'O servidor está fechado ou inacessível.'
    await interaction.response.send_message(status_message)

client.run(TOKEN)
