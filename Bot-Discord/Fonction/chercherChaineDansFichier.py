import json

def chercherChaineDansFichier(nom_fichier, chaine_a_chercher,channelid):

    # Initialisation ficher json
    dataOut = '{"message":"" , "ChannelID":""}'
    dataOut = json.loads(dataOut)
   
   # Spécifiez le chemin du fichier que vous souhaitez lire
    chemin_du_fichier = nom_fichier

    # Chaîne de caractères à rechercher
    chaine_recherchee = chaine_a_chercher

    # Ouvrez le fichier en mode lecture
    with open(chemin_du_fichier, 'r') as fichier:
        lignes = fichier.readlines()  # Lire toutes les lignes du fichier

        # Parcourez chaque ligne pour rechercher la chaîne
        for numero_ligne, ligne in enumerate(lignes, start=1):
            # Comparaison exacte après suppression des espaces
           
            # Débug comparaison if chaîne trouvée
            #print("chaine rechercher : " , chaine_recherchee ," de type : " , type(chaine_recherchee))
            #print("ligne comparé : " , ligne.split("§")[1] ," de type : " , type(ligne.split("§")[1]))

            if str(chaine_recherchee) == str(ligne.split("§")[1]):  
                             
                dataOut["message"] = "Chaine trouvée"
                dataOut["ChannelID"] = ligne.split("§")[0]
                return dataOut

    # Si la chaîne n'est pas trouvée, vous pouvez afficher un message
    if all(chaine_recherchee != ligne.strip() for ligne in lignes):
        
        dataOut["message"] = "Chaine non Trouvée"
        return dataOut


