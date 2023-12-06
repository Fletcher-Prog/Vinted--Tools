import requests
import Fonction as mypackage


def recupArticle(link):

    # Récupération du derrniére article en fonction du lien 
    #linkApi = 'http://172.26.5.140:5000/vinted?'+link
    linkApi = 'http://127.1.1.1:5001/vinted?'+link
    
    # Debug link
    #print(link)  
    
    # Uniformalisation des données
    reponse = requests.get(linkApi).json()

    mypackage.log_RecuperationDonneApi.info("lien reçu : {} réponse {}".format(link, reponse))

    return reponse