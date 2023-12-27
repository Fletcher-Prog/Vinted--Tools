import json

import Fonction as mypackage

def chercherChaineDansFichier(nom_fichier, chaine_a_chercher,rechercheParChannelid=False):

       
   # Spécifiez le chemin du fichier que vous souhaitez lire
    chemin_du_fichier = nom_fichier

    # Chaîne de caractères à rechercher
    chaine_recherchee = chaine_a_chercher

    # Ouvrez le fichier en mode lecture
    with open(chemin_du_fichier, 'r') as fichier:
        lignes = fichier.readlines()  # Lire toutes les lignes du fichier

    if rechercheParChannelid == False : 
        
        # Initialisation ficher json
        dataOut = '{"message":"" , "ChannelID":"" , "indexChaine":""}'
        dataOut = json.loads(dataOut)

        # Parcourez chaque ligne pour rechercher la chaîne
        for numero_ligne, ligne in enumerate(lignes, start=1):
            # Comparaison exacte après suppression des espaces
        
            # Débug comparaison if chaîne trouvée
            # print("chaine rechercher : " , chaine_recherchee.lower() ," de type : " , type(chaine_recherchee))
            # print("ligne comparé : " , ligne.split("§")[1].lower() ," de type : " , type(ligne.split("§")[1]))
            # (str(chaine_recherchee).lower() , str(ligne.split("§")[1]).lower())
            
            
            if mypackage.comparaisonEntre2Chaine(str(chaine_recherchee) , str(ligne.split("§")[1])) :  
                
                dataOut["message"]   = "Chaine trouvée"
                dataOut["ChannelID"] = ligne.split("§")[0]
                dataOut["indexChaine"]     = (numero_ligne -1)

                mypackage.log_ComparaisonEntre2Chaine.info("nom ficher : {} , chaine a rechercher : {} , channeid {} : , le resulta {} ".format(nom_fichier , chaine_recherchee , ligne.split("§")[0] , dataOut))

                return dataOut

        # Si la chaîne n'est pas trouvée, vous pouvez afficher un message
        if all(chaine_recherchee != ligne.strip() for ligne in lignes):
            
            dataOut["message"] = "Chaine non Trouvée"

            mypackage.log_ComparaisonEntre2Chaine.info("nom ficher : {} , chaine a rechercher : {} , channeid {} : , le resulta {} ".format(nom_fichier , chaine_recherchee , ligne.split("§")[0] , dataOut))
            
            return dataOut
        
    else:   

         # Initialisation ficher json
        dataOut = '{"message":"" , "Chaine":"" , "indexChannelid":""}'
        dataOut = json.loads(dataOut)


        # Parcourez chaque ligne pour rechercher la chaîne
        for numero_ligne, ligne in enumerate(lignes, start=1):
            # Comparaison exacte après suppression des espaces
        
            # Débug comparaison if chaîne trouvée
            # print("chaine rechercher : " , chaine_recherchee.lower() ," de type : " , type(chaine_recherchee))
            # print("ligne comparé : " , ligne.split("§")[1].lower() ," de type : " , type(ligne.split("§")[1]))
            # (str(chaine_recherchee).lower() , str(ligne.split("§")[1]).lower())
            
            
            if mypackage.comparaisonEntre2Chaine(str(chaine_recherchee) , str(ligne.split("§")[0])) :  
                
                dataOut["message"]            = "Chaine trouvée"
                dataOut["Chaine"]             = ligne.split("§")[1]
                dataOut["indexChannelid"]     = (numero_ligne -1)

                mypackage.log_ComparaisonEntre2Chaine.info("nom ficher : {} , chaine a rechercher : {} , channeid {} : , le resulta {} ".format(nom_fichier , chaine_recherchee ,  str(ligne.split("§")[0]) , dataOut))

                return dataOut
            
            # Si la chaîne n'est pas trouvée, vous pouvez afficher un message
            if all(chaine_recherchee != ligne.strip() for ligne in lignes):
                
                dataOut["message"] = "Chaine non Trouvée"

                mypackage.log_ComparaisonEntre2Chaine.info("nom ficher : {} , chaine a rechercher : {} , channeid {} : , le resulta {} ".format(nom_fichier , chaine_recherchee , ligne.split("§")[0] , dataOut))
                
                return dataOut
    
    
    
