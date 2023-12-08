import javax.swing.*;
import java.awt.*;


public class Ihm extends JFrame
{
	// Panelle overlay droite
	private JPanel panelOverlayDroite = new JPanel(new FlowLayout()) ;
	private JPanel panelOverlayHaut   = new JPanel(new FlowLayout(FlowLayout.CENTER)) ;
	private JButton buttonPassageLog        = new JButton("Log");



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
		
		// Construction de l'overlay 
		overlay();

		// Rendre la fenetre soit visible
        this.setVisible(true);

    }

	public  void overlay()
	{
		// Contruction est ajout de l'overlay
		panelOverlayDroite.setPreferredSize(new Dimension(55 , 50 ));
		panelOverlayDroite.setBackground(Color.BLACK) ;

		panelOverlayHaut.add(buttonPassageLog , BorderLayout.CENTER);
		panelOverlayHaut.setPreferredSize(new Dimension(50 , 50 ));
		panelOverlayHaut.setBackground(Color.BLACK) ;
		
		
		// Ajout de l'overlay
		this.add(panelOverlayDroite, BorderLayout.WEST );
		this.add(panelOverlayHaut, BorderLayout.NORTH );


		
	}

    public static void main(String[] args)
    {
        new Ihm();
    }



}