import javax.swing.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.awt.*;
import java.io.InputStream;


public class Ihm extends JFrame
{
	// Panel overlay droite
	private JPanel     panelOverlayDroite      = new JPanel(new FlowLayout()) ;
	private JPanel     panelOverlayHaut        = new JPanel(new FlowLayout(FlowLayout.CENTER)) ;
	
	// Pannel log et requette
	private JPanel     pannelLog               = new JPanel(new FlowLayout(FlowLayout.RIGHT));
	private JPanel     pannelRequette          = new JPanel(new FlowLayout(FlowLayout.RIGHT));
	
	// Boutton de pasage entre les pannels
	private JButton    buttonPassageLog        = new JButton("Log");
	private JButton    buttonPassageRequette   = new JButton("Requette");
	
	// Couleur personaliser
	private Color      couleurPannelLog        =  new Color(0xFFA500); 
	private Color      couleurPannelReqette    =  new Color(0x0000FF);
	private Color      couleurPannelOverlay    =  new Color(0x252525);
	
	// Permet le switch entre les pannel sans les re construire
	private CardLayout listePannel             = new CardLayout();
	private JPanel     listeDesPannel          = new JPanel(listePannel);

	// Creation du systeme de scroling text panel log 
	private JTextArea log = new JTextArea();
	private JScrollPane scrolPanelLog = new JScrollPane(log) ;

	// Creation du systeme de scroling text panel requette 
	private  JTextArea requette = new JTextArea();
	private  JScrollPane scrolPanelRequette = new JScrollPane(requette) ;

	private String ligneAjouter ;



	// Constructucteur
    public Ihm()
    {
        super("Api vinted");
		
		// Fermeture de la fentre quand on appui sur la croix rouge
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
		// Title de la fenetre
		this.setSize(500, 500);

		this.setBackground(Color.WHITE);

		// Rendre la fentre non redimentionnable
		this.setResizable(false);
		
		// Changement de pannel en fonction du boutton appuiyer
		buttonPassageLog.addActionListener(new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				listePannel.show(listeDesPannel,"pannelLog");
				
			}
		});
		
		buttonPassageRequette.addActionListener(new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				listePannel.show(listeDesPannel,"pannelRequette");
			}
		});	


		// Construction de l'overlay 
		overlay();
		
		// Construction du pannel requette
		pannelDesRequette();
		
		// Construction du pannel des logs
		pannelDesLog();

		// Ajou des pannels grace a la liste
		this.add(listeDesPannel, BorderLayout.CENTER);
		
		// Rendre la fenetre soit visible
        this.setVisible(true);

		// Creation de plusieurs instance de la fonction lastLigneOfFile
		ExecutorService executorService = Executors.newFixedThreadPool(2);

		// Permet  d'attribuer les tache au thread
        executorService.submit(() -> lastLigneOfFile("requettes.txt", requette));
        executorService.submit(() -> lastLigneOfFile("log.txt", log));

    }

	// Construction de l'overlay
	private void overlay()
	{
		// Contruction des ajout pour l'overlay
		panelOverlayDroite.setPreferredSize(new Dimension(55 , 50 ));
		panelOverlayDroite.setBackground(couleurPannelOverlay) ;

		panelOverlayHaut.setPreferredSize(new Dimension(50 , 50 ));
		panelOverlayHaut.setBackground(couleurPannelOverlay) ;
		
		// Ajout des element au pannel 
		this.add(panelOverlayDroite, BorderLayout.WEST );
		this.add(panelOverlayHaut, BorderLayout.NORTH );
		panelOverlayHaut.add(buttonPassageRequette , BorderLayout.CENTER);
		panelOverlayHaut.add(buttonPassageLog , BorderLayout.CENTER);		
	}

	// Pannel requette
	private void pannelDesRequette()
	{
		scrolPanelRequette.setPreferredSize(new Dimension(435,400));

		pannelRequette.add(scrolPanelRequette);

		listeDesPannel.add(pannelRequette,"pannelRequette") ;
	}

	// Pannel de log
	private void pannelDesLog()
	{
		scrolPanelLog.setPreferredSize(new Dimension(435,400));

		pannelLog.add(scrolPanelLog);

		//this.add(pannelLog, BorderLayout.EAST) ;		
		listeDesPannel.add(pannelLog,"pannelLog") ;

	}

	private void lastLigneOfFile(String fileName, JTextArea namepannel)
	{
		String ligne ,lignePrecedente , lignes;

		lignePrecedente = " ";
		lignes = "";
		ligne = " ";

		 while (true) {
            
			try (BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(fileName), "UTF-8"))) {
            
				while ((lignes = br.readLine()) != null) {
					
					ligne = lignes;
        
				}

                // Si la dernière ligne n'est pas null et est différente de la précédente, l'afficher
                if (lignePrecedente != null && !lignePrecedente.equals(ligne)) {
					
					ligneAjouter = ligne ;
					
					// Permet de mettre a jour l'inteface sans être sur le thread UI Graphique
					SwingUtilities.invokeLater(() -> namepannel.append(ligneAjouter + "\n"));       
					
					//System.out.println(ligne);
					
					lignePrecedente = ligne;
        
				}

                Thread.sleep(1000);
            } 
			catch (Exception e) {
            
				System.out.println("Erreur lors de la lecture du fichier : " + e.getMessage());
            
			}
        }
	}



    public static void main(String[] args)
    {
		// Lancement de la parti python de l'api 
		String cheminApi = System.getProperty("mainApi.py");
		
		// Commande pour exécuter le script Python
		String command = "python3 " + cheminApi;
		try
		{
			ProcessBuilder partpython = new ProcessBuilder(command.split("\\s"));
			Process process = partpython.start();
		}
		
		catch (Exception e)
		{

		}

		
		// Instanciation de l'Ihm
        new Ihm();

		
    }



}