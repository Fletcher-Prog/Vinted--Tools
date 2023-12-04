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


def last_publish(url):

        # Créatoin d'un obke json pour avoir un retun propre
        dataOut = '{"name": "" , "marque": "" , "taille": "" , "priceHTT": "" , "priceTTC": "" , "linkImg": "" , "idProduit" : "" , "Error" : "" , "MsgError" : ""}'
        dataOut = json.loads(dataOut)

        # Initiatisation de ERROR a Faux
        dataOut["Error"] = "False"

        #Auto install Driver et config web driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--headless')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-plugins-discovery")
        bot = webdriver.Chrome(options=options,  executable_path="./Chrome+Webdriver/chromedriver")
        bot.set_window_size(1680, 900)
        
        stealth(bot,
                languages=["fr-FR", "fr"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        
        # Gestion de l'erreur en cas d'abscense de connection 
        try :
                bot.get(url)
        except Exception as e :
                
                erreurRencontre = str(e)
                
                messageErreurAttendu = "net::ERR_INTERNET_DISCONNECTED"

                if messageErreurAttendu in erreurRencontre :
                        
                        dataOut["Error"] = "True"
                        dataOut["MsgError"] = "La connextion internet est rompu" 

        # Attente chargement page
        #time.sleep(time_wait_charging_page)

        # Spécifie le temps d'attente maximal en secondes
        temps_attente_maximal = 35


        # Attente du chargement de la page
        try:
                WebDriverWait(bot, temps_attente_maximal).until((EC.presence_of_all_elements_located(By.XPATH,"//button[@data-testid='catalog--catalog-filter--trigger'']")))
                
                # À ce stade, la page est considérée comme chargée
                print("La page est complètement chargée!")

        finally:
                # Recuperation de plusieure info sur l'annonce d'on Name PriceHTT Marque Taille
                try:        
                        # Afficher les infos recupére
                        #print(Links_description.text)
                        Links_description = bot.find_element(By.XPATH ,'//div[@class="feed-grid__item-content"]')        

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

                # Recupe prix tout taxe
                try:
                        price_TTC = bot.find_element(By.XPATH , "//h4[@class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left web_ui__Text__primary']" ).text
                except:
                        dataOut["Error"] = "True"
                        price_TTC = "Erreur lors de la récupération du prix" 

                # Récupération du lien de l'annonce
                try :
                        lienAnnonce = bot.find_element(By.XPATH , ' //a[@class="new-item-box__overlay new-item-box__overlay--clickable"]')
                        lienAnnonce = lienAnnonce.get_attribute("href")
                except:
                        dataOut["Error"] = "True"
                        lienAnnonce = "Erreur lors de la récupération du prix" 

                # Recuper le lien de l'image
                try : 
                        Img =  bot.find_element(By.XPATH , "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']/img[@class='web_ui__Image__content']" ).get_attribute("src")
                except:
                        dataOut["Error"] = "True"
                        Img = "Erreur lors de la récupération de l'image" 

                
                # Mise a jours de l'objet json pour avoir les données recupére 
                dataOut["name"] = name
                dataOut["marque"] = marque
                dataOut["taille"] = taille
                dataOut["priceHTT"] = priceHTT
                dataOut["priceTTC"] = price_TTC
                dataOut["linkImg"] = Img
                dataOut["LienAnnonce"] = lienAnnonce

                #print(dataOut)

                # Downolad Img
                #Img =  bot.find_element(By.XPATH , "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']/img[@class='web_ui__Image__content']" ).get_attribute("src")
                
                #bot.get(Img)

                #print(dataOut)

                return dataOut
        


print(last_publish('https://www.vinted.fr/catalog?search_text=sweat%20lacoste&price_to=15&currency=EUR&size_ids[]=207&size_ids[]=208&status_ids[]=1&status_ids[]=2&order=newest_first'))
