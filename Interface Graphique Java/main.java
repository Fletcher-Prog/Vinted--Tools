import javax.swing.*;
import java.awt.*;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;


public class Ihm extends JFrame 
{

	private JLabel label ;
	private JLabel label1 ;
	private JPanel cartes;
    private CardLayout gestionnaireCartes;


	// Création de pannel 
	private JPanel panelRequette = new JPanel(new FlowLayout());
	private JPanel panelLog = new JPanel(new FlowLayout());
	
	// Création de boutton 
	private	JButton boutonRequettes = new JButton("Requettes");	
	private	JButton boutonLog = new JButton("Log");

	

	public Ihm()
	{
		super(" Api Vinted ");

		cartes = new JPanel();
        gestionnaireCartes = new CardLayout();
        cartes.setLayout(gestionnaireCartes);

		panelRequette() ;
		panelLog() ;

		

		// Arréter le programme aprés la fermeture de la fenetre 
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		// Taille de la fenetre 
		this.setSize(500,500);

		// Posibilite de redimentionner la fenetre
		setLocationRelativeTo(null);		
		

		// Ajuste la position du lable²²
			addComponentListener(new ComponentAdapter() 
		{	
			@Override
			public void componentResized(ComponentEvent e)
			{
				ajusterPosition();
			}
		});


		cartes.add(panelRequette, "panelRequette");
        cartes.add(panelLog, "panelLog");

		add(cartes);

		this.setVisible(true);

	}


	public static void main(String[] args)
	{
		SwingUtilities.invokeLater(Ihm::new);
	}


	// Ajuste la positon relativement a la fenetre 
	private void ajusterPosition()
	{
		// obtenir la largeur  de la fenetre 
		int largeurFenetre = getWidth();

		// Obtenir la longeur de la fenetre
		int longeurFenetre = getHeight();

		// calculer la position du label 
		int xlabel = ( largeurFenetre - label.getHeight() ) / 2 ;
		int ylabel = ( longeurFenetre - label.getHeight() ) / 2 ;

		// Definir la nouvelle position du label 
		label.setLocation(xlabel,ylabel);
		label1.setLocation(xlabel,ylabel);

	}


	public void panelRequette()
	{
		// Création et ajoue du texte a la fenetre
		label = new JLabel("Thread Annonce");
		panelRequette.add(label);


		boutonRequettes.addActionListener(new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				 gestionnaireCartes.show(cartes, "panelRequette");
			}
		});
		

		// Ajout des bouttons
		//panelRequette.add(boutonRequettes);
		panelRequette.add(boutonLog);

	}


	public void panelLog()
	{
		// Création et ajoue du texte a la fenetre
		label1 = new JLabel("test");
		panelLog.add(label1);

		boutonLog.addActionListener(new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				 gestionnaireCartes.show(cartes, "panelLog");
			}
		});

		// Ajout des bouttons
		panelLog.add(boutonRequettes);
		//panelLog.add(boutonLog);

	}


	
	
}