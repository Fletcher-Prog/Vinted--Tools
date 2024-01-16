import re

def delete(file_path,elementASupprimer):

    # Lire le fichier
    with open(file_path, 'r') as file:
        content = file.read()

    
    if elementASupprimer in content:
        # Remplacer les URL par un espace, puis supprimer les espaces supplémentaires
        content_without_urls = re.sub(elementASupprimer, ' ', content).strip()
        modified_content = re.sub(r'\s+', '\n', content_without_urls)

        # Écrire le contenu modifié dans le fichier
        with open(file_path, 'w') as file:
            file.write(modified_content)
            file.close()
        
        return True
    
    else :
        return False
