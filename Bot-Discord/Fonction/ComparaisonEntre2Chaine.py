import Fonction as mypackage

def comparaisonEntre2Chaine(DernierNomAnnonce,NomActuelAnnonce) :
	
	if DernierNomAnnonce != NomActuelAnnonce :
		
		mypackage.log_ComparaisonEntre2Chaine.info("1er chaine : {} 2éme chaine : {} Resulta : true".format(DernierNomAnnonce , NomActuelAnnonce))

		return False
	
	mypackage.log_ComparaisonEntre2Chaine.info("1er chaine : {} 2éme chaine : {} Resulta : true".format(DernierNomAnnonce , NomActuelAnnonce))
	
	return True