import Fonction as mypackage

def comparaisonEntre2Chaine(DernierNomAnnonce,NomActuelAnnonce) :

	DernierNomAnnonce = DernierNomAnnonce.lower().strip()
	NomActuelAnnonce  = NomActuelAnnonce.lower().strip()
	
	if DernierNomAnnonce != NomActuelAnnonce :
		
		mypackage.log_ComparaisonEntre2Chaine.info("1er chaine : {} 2éme chaine : {} Resulta : false".format(DernierNomAnnonce , NomActuelAnnonce))

		return False
	
	else :
		mypackage.log_ComparaisonEntre2Chaine.info("1er chaine : {} 2éme chaine : {} Resulta : true".format(DernierNomAnnonce , NomActuelAnnonce))
		return True