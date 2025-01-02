import requests
from bs4 import BeautifulSoup



url ="https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first"

agents = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'}

html_content = requests.get(url, headers = agents ).text

print(html_content)

#if html_content.status_code == 200 :
	
pageRepondu = BeautifulSoup(html_content, 'html.parser')


pageRepondu.find('//div[@class="feed-grid__item-content"]') 

# Écrire le contenu HTML dans un fichier
with open("page.html", "w", encoding="utf-8") as file:
    file.write(str(pageRepondu.find('div[@class="feed-grid__item-content"]')) )