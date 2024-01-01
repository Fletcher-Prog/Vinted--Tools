from selenium import webdriver
import time
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import json
import logging


def last_publish(url):
        while True : 
                try :
                        erreur = False

                        # Configuration du système de logs
                        logging.basicConfig(filename='Api Vinted/Fonction/last_publish.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
                        
                        # Créatoin d'un obke json pour avoir un retun propre
                        dataOut = '{"name": "" , "marque": "" , "taille": "" , "priceHTT": "" , "linkImg": "" , "idProduit" : "","titreAnnonce": "" , "Error" : "" , "MsgError" : ""}'
                        dataOut = json.loads(dataOut)

                        # Initiatisation de ERROR a Faux
                        dataOut["Error"] = "False"

                        #Auto install Driver et config web driver
                        options = webdriver.ChromeOptions()
                        options.add_argument("--disable-software-rasterizer")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--disable-accelerated-2d-canvas")
                        options.add_argument("--disable-gpu")
                        options.add_argument("--disable-extensions")
                        options.add_argument("--disable-popup-blocking")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-logging")
                        options.add_argument("--disable-plugins")
                        options.add_argument("--headless")
                        options.add_argument("--disable-software-rasterizer")

                        bot = webdriver.Chrome(options=options, )
                       # bot.set_window_size(1680, 900)
                        
                        stealth(bot,
                                languages=["fr-FR", "fr"],
                                vendor="Google Inc.",
                                platform="Win32",
                                webgl_vendor="Intel Inc.",
                                renderer="Intel Iris OpenGL Engine",
                                fix_hairline=True,
                                )
                                
                        # Si il ne trouve pas un element il va le cherche pendant 15 secondes avant de génere une execpetion 
                        bot.implicitly_wait(15)
                        
                        # Gestion de l'erreur en cas d'abscense de connection 
                        while True :
                               
                                try :
                                        dataOut["Error"] = "False"      
                                        bot.get(url)
                                
                                except Exception as e :
                                        
                                        erreurRencontre = str(e)
                                        
                                        messageErreurAttendu = "net::ERR_INTERNET_DISCONNECTED"

                                        if messageErreurAttendu in erreurRencontre :
                                                
                                                dataOut["Error"] = "True"
                                                dataOut["MsgError"] = "La connextion internet est rompu" 
                               
                                if dataOut["Error"] == "False":
                                        break
                                        

                        # Recuperation de plusieure info sur l'annonce d'on Name PriceHTT Marque Taille
                        try:    

                                Links_description = bot.find_element(By.XPATH ,'//div[@class="feed-grid__item-content"]')        
                                # Afficher les infos recupére
                                #print(Links_description.text)

                                list_Name_PriceHTT_Marque_Taille = Links_description.text

                                list_Name_PriceHTT_Marque_Taille = list_Name_PriceHTT_Marque_Taille.split("\n")

                                name = list_Name_PriceHTT_Marque_Taille[0].split(",")
                                name = name[0]

                                priceHTT = list_Name_PriceHTT_Marque_Taille[1].replace(", marque" , " ")

                                marque = list_Name_PriceHTT_Marque_Taille[5].split(",")
                                marque = marque[0]

                                taille = list_Name_PriceHTT_Marque_Taille[4]
                        except:
                                dataOut["Error"] = "True"
                                list_Name_PriceHTT_Marque_Taille = name = priceHTT = marque =taille = " Erreure bloc de récpération de l'annonce "


                        # Récupération du lien de l'annonce
                        try :
                                lienAnnonce = bot.find_element(By.XPATH , ' //a[@class="new-item-box__overlay new-item-box__overlay--clickable"]')
                                lienAnnonce = lienAnnonce.get_attribute("href")
                        except:
                                dataOut["Error"] = "True"
                                lienAnnonce = "Erreur lors de la récupération du lien" 

                        # Recuper le lien de l'image
                        try : 
                                Img =  bot.find_element(By.XPATH , "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']/img[@class='web_ui__Image__content']" ).get_attribute("src")
                        except:
                                dataOut["Error"] = "True"
                                Img = "Erreur lors de la récupération de l'image" 

                        # A tester !!!!!!!
                        # Recuper le lien de le titre de l'annonce
                        try : 
                                titreAnnonce =  bot.find_element(By.XPATH , "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']/img[@class='web_ui__Image__content']" ).get_attribute("alt")
                        except:
                                dataOut["Error"] = "True"
                                titreAnnonce = "Erreur lors de la récupération du titre" 
                                                        
                        # Mise a jours de l'objet json pour avoir les données recupére 
                        dataOut["name"]         = name
                        dataOut["marque"]       = marque
                        dataOut["taille"]       = taille
                        dataOut["priceHTT"]     = priceHTT
                        dataOut["linkImg"]      = Img
                        dataOut["LienAnnonce"]  = lienAnnonce
                        dataOut["titreAnnonce"] = titreAnnonce


                        #print(dataOut)
                        
                        if erreur == False :
                                
                                break
                except Exception as e :
                        erreure = True 
                        logging.error(e)

        bot.quit()
        return dataOut

#print(last_publish("https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first"))