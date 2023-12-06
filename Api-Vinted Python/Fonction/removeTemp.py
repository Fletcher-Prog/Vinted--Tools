# Scrip permetant de vider le cahe automatiquement 
import os 
import shutil


# Chemin du dossier temp

def removeTemp(cheminTemp):

	# Parcour tout les elments qui son dans l'emplacement ou pointe l'argument cheminTemp
	for element in os.listdir(cheminTemp):
		
		# print(element)
		
		if ".com.google.Chrome" in element :

			#print("Dossier temporaire chrome")

			cheminDossier = cheminTemp + "/" + element 

			# Permet de supprimer définitivement et de mainére récursive un dossier et son contenu
			shutil.rmtree(cheminDossier,ignore_errors=False, onerror=None)




