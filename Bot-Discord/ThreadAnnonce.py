import Fonction as mypackage
import asyncio
import concurrent.futures
import time

def run_blocking_function_sync_recupArticle(lienVinted):
    return mypackage.recupArticle(lienVinted)

def run_blocking_function_sync_creationEmbed(annonce):
    return mypackage.creationEmbed(annonce)


async def threadAnnonce(lienVinted,channelid):



	loop = asyncio.get_event_loop()

	while True :
		
		annonce = await asyncio.to_thread(run_blocking_function_sync_recupArticle, lienVinted)

		lienAnnonce = annonce["LienAnnonce"].strip()

		

		# Vefrification de l'intégriter des donnée
		if annonce["Error"] == "False" :

			if lienAnnonce not in mypackage.vintedLinkPublish :

				embed , lienAnnonce = await asyncio.to_thread( run_blocking_function_sync_creationEmbed, annonce)

				button = mypackage.createButton("Voir L'anonnce",lienAnnonce)

				canal = mypackage.client.get_channel(channelid)

				# Ajoute du lien a la liste est suppresion du derniér lien pour avoir crée le décalage de 
				mypackage.vintedLinkPublish.insert(0,lienAnnonce)

				if len(mypackage.vintedLinkPublish) > 10 :
					mypackage.vintedLinkPublish.pop()

				#print("lienAnnonce                    : " ,lienAnnonce)

				if canal:				
					# Envoyez le message dans le canal spécifiécanal 
					messageLog = "envoyé du message pour le nouvel article dans le canal : {} lienAnnonce : {} ".format(canal, lienAnnonce)

					mypackage.log_threadAnnonce.info(messageLog)
					
					msg = asyncio.run_coroutine_threadsafe(envoyer(canal, embed, button ), mypackage.client.loop)
					msg.result()			
				else:
					print("Canal non trouvé.")
			
			

			time.sleep(5)
		#print("lien égale")


async def envoyer(canal , embed , button):
		
		await canal.send(embed=embed, view=button)
