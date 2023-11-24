
fileLink = "links.txt"

while True :

    with open(fileLink,"r+") as ficher :
        lignes = ficher.readlines()

    print(lignes)
    