import Fonction as myfonction
from Fonction import client 
import asyncio
import concurrent.futures

def run_blocking_function_sync_recupArticle(lienVinted):
    return myfonction.recupArticle(lienVinted)

def run_blocking_function_sync_creationEmbed(annonce):
    return myfonction.creationEmbed(annonce)


async def threadAnnonce(lienVinted,channelid):


	ancientLienAnnonce = " "

	loop = asyncio.get_event_loop()

	while True :
		
		annonce = await asyncio.to_thread(run_blocking_function_sync_recupArticle, lienVinted)

		lienAnnonce = annonce["LienAnnonce"]
		
		#print(lienAnnonce)

		if myfonction.comparaisonEntre2Chaine(ancientLienAnnonce,lienAnnonce) == False:

			embed , lienAnnonce = await asyncio.to_thread( run_blocking_function_sync_creationEmbed, annonce)

			button = myfonction.createButton("Voir L'anonnce",lienAnnonce)

			canal = client.get_channel(channelid)

			if canal:
				
				# Envoyez le message dans le canal spécifié
				print(canal)
				msg = asyncio.run_coroutine_threadsafe(envoyer(canal, embed, button ), client.loop)
				msg.result()			
			else:
				print("Canal non trouvé.")
			
			ancientLienAnnonce = lienAnnonce

		#print("lien égale")


async def envoyer(canal , embed , button):
	
		await canal.send(embed=embed, view=button )
