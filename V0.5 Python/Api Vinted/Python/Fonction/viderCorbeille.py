import subprocess


def viderCorbeille():
	
	try : 
		
		subprocess.run(["gio", "trash", "--empty"])

	except Exception as e: 
		print("Erreur lors de vider la corbeille",str(e))