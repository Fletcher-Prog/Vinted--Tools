def tri(nom_ficher:str,spliter:str): 
   # Ouverture Ficher en mode lecture ("r")
    links_txt = open(nom_ficher,"r")
    print('links_txt : ' + str(links_txt))
    # Lecture de toutes les lignes du ficher
    links_txt = links_txt.readlines()
    print('links_txt : ' + str(links_txt))
    # Recuperation nombre de ligne
    nb_liens = len(links_txt)
    print('nb_liens : '+ str(nb_liens))
    # Liste de tout les liens bien ordonnée en fonction du nom 
    reslta = []
    print('reslta : ' + str(reslta))

    nb_depart = 0
    # Split entre le nom et le lien
    while nb_depart != nb_liens :
        nb_liens = nb_liens - 1
        reslta.append(links_txt[nb_liens].split(spliter))
        nb_depart += 1
    return reslta