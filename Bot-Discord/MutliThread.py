import threading
from ThreadAnnonce import * 
import time
import warnings

# récperer le nombre de ligne utilisé dans un ficher
fileLink = "links.txt"

def multhread():
    
    nblignesPrecedant = 0

    while True : 

        with open(fileLink,"r") as ficher :
            lignes = ficher.readlines()
 
        nblignes = len(lignes)
        indexLigneActuelle = 0

        if nblignes > 0 : 
            if nblignesPrecedant != nblignes :
                # Parcour de tout les lignes du ficher de lien
                for ligne in enumerate(lignes, start=nblignesPrecedant):
                    
                    lien = ligne[1].split('§')[1]
                    channelid = int(ligne[1].split('§')[0])

                    mon_thread = threading.Thread(target=lancer_thread, args=(lien , channelid) )
                    

                    # Démarrer le thread
                    mon_thread.start()


                    indexLigneActuelle += 1
                    nblignesPrecedant = indexLigneActuelle


        else :
            print("pas de lien")
        

        time.sleep(1)


def lancer_thread(lien , channelid):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(threadAnnonce(lien, channelid))
    loop.close()
