import requests


def recupArticle(link):

    # Récupération du derrniére article en fonction du lien 
    #linkApi = 'http://172.26.5.140:5000/vinted?'+link
    linkApi = 'http://10.245.23.238:5000/vinted?'+link
    
    # Debug link
    #print(link)  
    
    # Uniformalisation des données
    reponse = requests.get(linkApi).json()

    return reponse