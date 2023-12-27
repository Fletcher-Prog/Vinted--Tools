import discord
from discord.ext import commands

import Fonction as mypackage



def creationEmbed(reponse):
    


    # Création de l'embed avec les bonne données
    embed = discord.Embed(
         title = "Annonce Vinted"
    )

    # Ajout de différent chants
    embed.add_field(name="Marque : " , value=str(reponse["marque"]) , inline=False)
    embed.add_field(name="Taille : " , value=str(reponse["taille"]), inline=False)
    embed.add_field(name="Nom de Vendeur : " , value=str(reponse["name"]), inline=False)
    embed.add_field(name="Prix HT : " , value=str(reponse["priceHTT"]), inline=False)
    
    # Ajout de l'image le try permet que si l'api n'a pas pue recupére  le lien de l'image d'envoye quand même l'embed
    try:
        embed.set_image(url=str(reponse["linkImg"]))
    except:
    	print("")

    urlAnnonce = reponse["LienAnnonce"]
    

    return embed, urlAnnonce
