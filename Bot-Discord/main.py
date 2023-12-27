import discord
from discord.ext import *
import Fonction as mypackage
import requests
import time
import threading
from MutliThread import multhread


# Executer des que le robots reçois !link <lien>
@mypackage.client.command()
async def link(ctx, *args):
    
    # Lien vinted
    urlVinted = args[0]

    # Label du boutton
    label = "Voir Annonce" 

    # Récupération du derrniére article vinted en fonction d'un lien 
    annonce = mypackage.recupArticle(urlVinted)

    # Création de l'embed en fonction d'une annonce
    embed , urlAnnonce = mypackage.creationEmbed(annonce)

    await ctx.send(embed=embed, view=mypackage.createButton(label,urlAnnonce))

# Executer des que le robots reçois !addlink <lien>
@mypackage.client.command()
async def addlink(ctx, *args):
    
    # Récupérez l'ID du canal où la commande a été exécutée
    channel_id = ctx.channel.id

    # Récupération du lien 
    link = str(args[0]) 

    # Verification que le liens n'est pas déjà present 
    resultLink = mypackage.chercherChaineDansFichier(mypackage.fileLink,link)  
    
    # Debug if 
    # print(resultLink["message"])

    if resultLink["message"] == "Chaine trouvée" :

        # permet de récupere le nom du channel en fonction l'id : client.get_channel (int(resultLink["ChannelID"])).name
        await ctx.send("Le lien est déjà present dans la base il est associer au channel " + mypackage.client.get_channel (int(resultLink["ChannelID"])).name) 
  
    else:
        # Écriture du lien dans le fiche
        with open(mypackage.fileLink,'a') as file :
            file.write(str(channel_id) + mypackage.separateur + link + '\n')

        await ctx.send("Le lien a bien était ajouter a la base")


# Executer des que le robots reçois !viewlink 
@mypackage.client.command()
async def viewlink(ctx, *args):

    channelid = str(ctx.channel.id)

    result = mypackage.chercherChaineDansFichier("link.txt",channelid,True)

    result = mypackage.lectureDeFicheParIndex("link.txt",result["indexChannelid"])

    await ctx.send(result)

# Executer des que le robots reçois !clear <nb msg sup>
@mypackage.client.command()
async def clear(ctx, *args):
   
    # Récupérez le canal à partir du contexte
    channel = ctx.message.channel
    
    # Argument nombre de message a spprimer
    nombre_messages = int(args[0])

    # Récuper le channel dans le quelle faut encoyer en fonction d l'id
    channel = mypackage.client.get_channel(channel)

    # Permet de ne pas dépasser le limite possible de suppréssion de message
    if nombre_messages > 100 :
        nombre_messages = 100

    # Verifi que la valuer est positif
    if nombre_messages <= 0:
            await ctx.channel.send("Veuillez fournir un nombre de messages positif à supprimer.")
    
    # Utilisez la méthode purge pour effacer tous les messages dans le canal
    await ctx.channel.purge(limit=nombre_messages)

# Executer des que le robots est allumer
@mypackage.client.event
async def on_ready():
    print(f'We have logged in as {mypackage.client.user}')
    
    # Créer un thread avec la gestion est création des thread en fonction des liens
    mon_thread = threading.Thread(target=multhread )

    # Démarrer le thread
    mon_thread.start()

mypackage.client.run("MTE4NzQ4OTg0NDU0NTQ2MjMwMg.GmeD6P.Ocy-tQ-yGdSqA48cNqvn24Ar1aBluUo4Eh8mpQ")
