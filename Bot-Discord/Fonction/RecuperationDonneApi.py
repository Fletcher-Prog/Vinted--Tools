import requests
import Fonction as mypackage


def recupArticle(link):

    # Récupération du derrniére article en fonction du lien 
    #linkApi = 'http://172.26.5.140:5000/vinted?'+link
    linkApi = 'http://127.1.1.1:5004/vinted'
    
    # Debug link
    #print(link)  

    headers = {"LienVinted": link }
    
    # Uniformalisation des données
    reponse = requests.get(linkApi, params=headers).json()
    
    if reponse["Error"] == "True":
        mypackage.log_RecuperationDonneApi.info("lien reçu : {} réponse {}".format(link, reponse))

    return reponse
