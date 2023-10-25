import requests

reponse = requests.get('http://127.0.0.1:3000/vinted?https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first').json()

# exemple
print(reponse['marque'])