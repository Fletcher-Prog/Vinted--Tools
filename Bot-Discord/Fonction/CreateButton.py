from discord.ui import Button, View
import discord

# Permet de crée un boutton a ajouter a un message

def createButton(label, urlAnnonce):
	
	button = Button(label=label, style=discord.ButtonStyle.link, url=urlAnnonce)
    
	view = View()
    
	view.add_item(button)

	return view