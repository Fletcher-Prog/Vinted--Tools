def lectureDeFicheParIndex(nom_fichier, index):
    try:
        # Ouvrir le fichier en mode lecture
        with open(nom_fichier, 'r') as fichier:
            # Lire toutes les lignes du fichier
            lignes = fichier.readlines()

            # Vérifier si l'index est dans la plage des lignes
            if 0 <= index < len(lignes):
                # Récupérer le contenu de la ligne à l'index spécifié
                contenu_ligne = lignes[index].strip()
                return contenu_ligne
            else:
                return f"L'index {index} est hors de la plage des lignes du fichier."

    except FileNotFoundError:
        return f"Le fichier {nom_fichier} n'a pas été trouvé."