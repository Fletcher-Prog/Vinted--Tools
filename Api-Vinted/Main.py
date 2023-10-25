
# For Launch mode debug : FLASK_APP=Main.py flask run

import Fonction as myfonction
from flask import Flask, render_template, request, g, current_app
import json

#Links_and_name = myfonction.tri("Links.txt","§")
#print(Links_and_name)
#print(myfonction.last_publish('https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first'))
#Lien exemple : http://127.0.0.1:3008/vinted?https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first

app = Flask(__name__)

@app.route('/')
def index():
    return 'L\'api marche'


@app.route('/vinted')
def Vinted_last_publish():

    #Argument en praramétre
    link=request.args.get("link")
    link = str(request.query_string).replace("b'","")
    result = myfonction.last_publish(str(link))
    print(link)
    return result



if __name__ == '__main__':
    app.run(host='10.245.23.238', port=5000)
