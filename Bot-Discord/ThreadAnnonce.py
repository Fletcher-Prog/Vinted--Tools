import Fonction as mypackage
import asyncio
import concurrent.futures
import time

def run_blocking_function_sync_recupArticle(lienVinted):
    return mypackage.recupArticle(lienVinted)

def run_blocking_function_sync_creationEmbed(annonce):
    return mypackage.creationEmbed(annonce)


async def threadAnnonce(lienVinted,channelid):


	precedantPrecedantLienAnnonce = " "
	precedantLienAnnonce            = " "

	loop = asyncio.get_event_loop()

	while True :
		
		annonce = await asyncio.to_thread(run_blocking_function_sync_recupArticle, lienVinted)

		lienAnnonce = annonce["LienAnnonce"]
		
		print(lienAnnonce)

		# Vefrification de l'intégriter des donnée
		if annonce["Error"] == "False" :

			if mypackage.comparaisonEntre2Chaine(precedantPrecedantLienAnnonce,lienAnnonce) == False |  mypackage.comparaisonEntre2Chaine(precedantLienAnnonce,lienAnnonce) == False :

				embed , lienAnnonce = await asyncio.to_thread( run_blocking_function_sync_creationEmbed, annonce)

				button = mypackage.createButton("Voir L'anonnce",lienAnnonce)

				canal = mypackage.client.get_channel(channelid)

				precedantPrecedantLienAnnonce = precedantLienAnnonce
				precedantLienAnnonce = lienAnnonce		
				#print ("precedantPrecedantLienAnnonce : " ,precedantPrecedantLienAnnonce)
				#print ("precedantLienAnnonce          : " ,precedantLienAnnonce)
				#print("lienAnnonce                    : " ,lienAnnonce)

				if canal:				
					# Envoyez le message dans le canal spécifiécanal 
					messageLog = "envoyé du message pour le nouvel article dans le canal : {} lienAnnonce : {} Ancient Lien Annonce : {}".format(canal, lienAnnonce, precedantLienAnnonce)

					mypackage.log_threadAnnonce.info(messageLog)
					
					msg = asyncio.run_coroutine_threadsafe(envoyer(canal, embed, button ), mypackage.client.loop)
					msg.result()			
				else:
					print("Canal non trouvé.")
			
			

			time.sleep(5)
		#print("lien égale")


async def envoyer(canal , embed , button):
		
		await canal.send(embed=embed, view=button)
