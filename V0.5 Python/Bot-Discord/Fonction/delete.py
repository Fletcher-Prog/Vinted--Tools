def delete(file_path,elementASupprimer):

    finalContent = ""

    with open(file_path,'r') as file : 
        content = file.readlines()

    #print(content)

    if elementASupprimer in content :

        for ligne in content :        

            if ligne.strip() != elementASupprimer.strip() :
                
                finalContent = finalContent + ligne

        with open(file_path,'w') as file : 
            file.write(finalContent)
            file.close
        
        return True

    else :

       return False
