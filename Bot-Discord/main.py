import discord
from discord.ext import commands
import requests

# https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first

# .json()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='$', intents=intents)

@client.command()
async def link(ctx, *args):
    link = 'http://127.0.0.1:3000/'+args[0]
    print(link)
    reponse = requests.get(link).json()
    print(reponse)
    await reponse

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run('MTE1MTg5MDg0ODM4NTA4NTUyMw.G1CWu5.ehGimOTqhjIZ_h1bGjkMhwuC7fOdTX7WIu_mmY')



