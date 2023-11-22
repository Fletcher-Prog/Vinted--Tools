import requests


def recupArticle(link):

    # Récupération du derrniére article en fonction du lien 
    linkApi = 'http://127.0.0.1:5000/vinted?'+link
    
    # Debug link
    #print(link)  
    
    # Uniformalisation des données
    reponse = requests.get(linkApi).json()

    return reponse