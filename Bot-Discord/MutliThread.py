import threading
from ThreadAnnonce import * 
import time

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
                for ligne in enumerate(lignes, start=0):
                    
                    lien = ligne[1].split('§')[1]
                    channelid = int(ligne[1].split('§')[0])

                    # Créer un thread
                    task_background = mypackage.client.loop.create_task(threadAnnonce(lien , channelid))
                    task_background.set_name("BackgroundTask")

                    indexLigneActuelle += 1
                    nblignesPrecedant = indexLigneActuelle

                
        
        

        else :
            print("pas de lien")
        

