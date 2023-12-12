import javax.swing.*;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import java.awt.*;


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
				listePannel.show(listeDesPannel,"pannelRequette");

			}
		});

		buttonPassageRequette.addActionListener(new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				listePannel.show(listeDesPannel,"pannelLog");
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

    }

	// Construction de l'overlay
	public  void overlay()
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
	public void pannelDesRequette()
	{
		pannelRequette.setPreferredSize(new Dimension(450,400));

		pannelRequette.setBackground(couleurPannelReqette);

		listeDesPannel.add(pannelRequette,"pannelRequette") ;
	}

	// Pannel de log
	public void pannelDesLog()
	{
		pannelLog.setPreferredSize(new Dimension(450,400));

		pannelLog.setBackground(couleurPannelLog);

		//this.add(pannelLog, BorderLayout.EAST) ;		
		listeDesPannel.add(pannelLog,"pannelLog") ;

	}

    public static void main(String[] args)
    {
        new Ihm();
    }

}