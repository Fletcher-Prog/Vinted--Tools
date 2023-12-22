
# For Launch mode debug : FLASK_APP=Main.py flask run
#Links_and_name = myfonction.tri("Links.txt","§")
#print(Links_and_name)
#print(myfonction.last_publish('https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first'))
#Lien exemple : http://127.0.0.1:3008/vinted?https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first

import Fonction as myfonction
from flask import Flask, render_template, request, g, current_app
import json
from waitress import serve
import threading
import time

# Lancement du thread pour vider le cache
cheminTemp: str = "/tmp"

# videCahe permet de vider le cache tant que le programe est allumer
def videCache(cheminTemp:str):
    
    while True :
        
        myfonction.removeTemp(cheminTemp)
    
        time.sleep(1/2)

        myfonction.viderCorbeille()

videCacheThread = threading.Thread(target=videCache, args=(cheminTemp, ), name="Vider Cache")

videCacheThread.start()

app = Flask(__name__)

import logging

# # Configurer le système de logs
# logging.basicConfig(level=logging.WARNING)


# # Config log
# historique_Requette = logging.getLogger()
# handler_Historique_Requette = logging.FileHandler("requettes.txt")
# handler_Historique_Requette.setLevel(logging.WARNING)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler_Historique_Requette.setFormatter(formatter)
# historique_Requette.addHandler(handler_Historique_Requette)
# # ecriture des logs
# @app.before_request
# def log_request_info():
#     historique_Requette.warning('Requête: {} {} {} ',request.remote_addr, request.method, request.url, 'Données de la requête: %s', request.get_data(as_text=True))



@app.route('/')
def index():
    return 'L\'api marche'


# Argument vinted pour l'api
@app.route('/vinted')
def Vinted_last_publish():
    
    #Argument en praramétre
    link=request.args.get("link")
    link = str(request.query_string).replace("b'","")

    # Envoie de l'argument en praramétre a la fonction last_publish
    result = myfonction.last_publish(str(link))
    
    #print(link)
    
    return result

if __name__ == '__main__':
    #app.run(host='172.26.5.140', port=5000)
    #app.run(host='127.0.0.1', port=5000)
    app.run(host='127.1.1.1', port=5004)
    #serve(app, host='127.0.0.1', port=5000)


        

    
