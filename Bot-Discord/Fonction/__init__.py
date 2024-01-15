from .chercherChaineDansFichier import *
from .RecuperationDonneApi import *
from .CreationEmbed import *    
from .CreateButton import *
from .variable import *
from .ComparaisonEntre2Chaine import *
from .lectureDeFicheParIndex import *

import discord
from discord.ext import commands


# Inisialisation du bot 
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

# Séparateur pour le ficher contenant les liens
separateur = '§'

# nom ficher contenant le liens
fileLink = 'links.txt'

# gestion des ficher log
import logging

# Configurer le système de logs
logging.basicConfig(level=logging.DEBUG)

# Création d'un logger pour chaque fichier de log
log_chercherChaineDansFichier = logging.getLogger("Log/chercherChaineDansFichier")
log_ComparaisonEntre2Chaine = logging.getLogger("Log/ComparaisonEntre2Chaine")
log_RecuperationDonneApi = logging.getLogger("Log/RecuperationDonneApi")
log_threadAnnonce = logging.getLogger("Log/threadAnnonce")

# Configurer un gestionnaire de fichier pour chaque logger
handler_chercherChaineDansFichier = logging.FileHandler("Log/chercherChaineDansFichier.txt")
handler_ComparaisonEntre2Chaine = logging.FileHandler("Log/ComparaisonEntre2Chaine.txt")
handler_RecuperationDonneApi = logging.FileHandler("Log/RecuperationDonneApi.txt")
handler_threadAnnonce = logging.FileHandler("Log/threadAnnonce.txt")

# Configurer le niveau de logs pour chaque gestionnaire de fichier
handler_chercherChaineDansFichier.setLevel(logging.INFO)
handler_ComparaisonEntre2Chaine.setLevel(logging.INFO)
handler_RecuperationDonneApi.setLevel(logging.INFO)
handler_threadAnnonce.setLevel(logging.INFO)

# Créer un formatteur de log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Attacher le formatteur à chaque gestionnaire de fichier
handler_chercherChaineDansFichier.setFormatter(formatter)
handler_ComparaisonEntre2Chaine.setFormatter(formatter)
handler_RecuperationDonneApi.setFormatter(formatter)
handler_threadAnnonce.setFormatter(formatter)

# Attacher les gestionnaires de fichier à chaque logger
log_chercherChaineDansFichier.addHandler(handler_chercherChaineDansFichier)
log_ComparaisonEntre2Chaine.addHandler(handler_ComparaisonEntre2Chaine)
log_RecuperationDonneApi.addHandler(handler_RecuperationDonneApi)
log_threadAnnonce.addHandler(handler_threadAnnonce)