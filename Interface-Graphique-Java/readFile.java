import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;

public class readFile {

	public static void main(String[] args)
	{
		String ligne , lignePrecedente , lignes;

		lignePrecedente = " ";
		lignes = "";
		ligne = " ";
		 while (true) {
            
			try (BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream("teste.txt"), "UTF-8"))) {
            
				while ((lignes = br.readLine()) != null) {
					
					ligne = lignes;
        
				}

                // Si la dernière ligne n'est pas null et est différente de la précédente, l'afficher
                if (lignePrecedente != null && !lignePrecedente.equals(ligne)) {
        
					System.out.println(ligne);
					lignePrecedente = ligne;
        
				}

                Thread.sleep(1000);
            } 
			catch (Exception e) {
            
				System.out.println("Erreur lors de la lecture du fichier : " + e.getMessage());
            
			}
        }
	}
}

