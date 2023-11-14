import discord
import Fonction as myfonction
from discord.ext import commands
import requests

# https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first

# .json()

intents = discord.Intents.default()
intents.message_content = True

# Séparateur pour le ficher contenant les liens
separateur = '§'

# nom ficher contenant le liens
fileLink = './links.txt'



client = commands.Bot(command_prefix='!', intents=intents)

@client.command()
async def link(ctx, *args):
    link = 'http://127.0.0.1:3000/'+args[0]
    print(link)
    reponse = requests.get(link).json()

    # Permet de récupére le channel associer a l'id entre prenthése+
    # bot.get_channel(int(channel_id))
    print(reponse)
    await reponse




@client.command()
async def addLink(ctx, *args):
    
    # Récupérez l'ID du canal où la commande a été exécutée
    channel_id = ctx.channel.id

    # Récupération du lien 
    link = str(args[0]) 

    # Verification que le liens n'est pas déjà present 
    resultLink = myfonction.chercher_chaine_dans_fichier(fileLink,link,channel_id)  
    print(resultLink["message"])
    if resultLink["message"] == "Chaine trouvée" :

        # permet de récupere le nom du channel en fonction l'id : client.get_channel (int(resultLink["ChannelID"])).name
        await ctx.send("Le lien est déjà present dans la base il est associer au channel " + client.get_channel (int(resultLink["ChannelID"])).name) 
  
    else:
        # Écriture du lien dans le fiche
        with open(fileLink,'a') as file :
            file.write(channel_id + separateur + link + '\n')

        await ctx.send("Le lien a bien était ajouter a la base")

@client.command()
async def clear(ctx, *args):
   
    # Récupérez le canal à partir du contexte
    channel = ctx.message.channel
    # Argument nombre de message a spprimer
    nombre_messages = int(args[0])

    # Permet de ne pas dépasser le limite possible de suppréssion de message
    if nombre_messages > 100 :
         nombre_messages = 100

    # Verifi que la valuer est positif
    if nombre_messages <= 0:
            await ctx.send("Veuillez fournir un nombre de messages positif à supprimer.")
            return
    
    # Utilisez la méthode purge pour effacer tous les messages dans le canal
    await channel.purge(limit=nombre_messages)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run('MTE1MTg5MDg0ODM4NTA4NTUyMw.G1CWu5.ehGimOTqhjIZ_h1bGjkMhwuC7fOdTX7WIu_mmY')
