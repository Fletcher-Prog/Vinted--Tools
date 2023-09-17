from selenium import webdriver
import time
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests


def last_publish(url,time_wait_charging_page:int=15):
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
        bot = webdriver.Chrome(options=options,  executable_path=ChromeDriverManager().install())
        bot.set_window_size(1680, 900)
        
        stealth(bot,
                languages=["fr-FR", "fr"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        bot.get(url)

        # Attente chargement page
        time.sleep(time_wait_charging_page)

        # Recuperation de plusieure info sur l'annonce d'on Name PriceHTT Marque Taille
        Links_description = bot.find_element(By.XPATH ,'//div[@class="feed-grid__item-content"]')
        print(Links_description)

        list_Name_PriceHTT_Marque_Taille = Links_description.text

        list_Name_PriceHTT_Marque_Taille = list_Name_PriceHTT_Marque_Taille.split("\n")

        name = list_Name_PriceHTT_Marque_Taille[0].split(",")
        name = name[0]

        priceHTT = list_Name_PriceHTT_Marque_Taille[1].replace(", marque" , " ")

        marque = list_Name_PriceHTT_Marque_Taille[5].split(",")
        marque = marque[0]

        taille = list_Name_PriceHTT_Marque_Taille[4]


        # Recupe prix tout taxe
        price_TTC = bot.find_element(By.XPATH , "//h4[@class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left web_ui__Text__primary']" ).text

        # Downolad Img
        #Img =  bot.find_element(By.XPATH , "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']/img[@class='web_ui__Image__content']" ).get_attribute("src")
        Img =  bot.find_element(By.XPATH , "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']/img[@class='web_ui__Image__content']" ).get_attribute("src")

        bot.get(Img)

        return name , marque , taille, priceHTT , price_TTC , Img