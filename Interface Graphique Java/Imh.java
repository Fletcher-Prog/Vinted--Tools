import javax.swing.*;
import java.awt.*;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
	

public class Ihm extends JFrame {

	public Ihm() {

		// Variable
		JLabel label = new JLabel("Bonjour, c'est ma fenêtre !") ;

		// Titre de la fenetre 
		this.setTitle("Api Vinted V1.0");

		// Taille de la fenetre
		this.setSize(400,400);

		// Fermeture de la fenetre lors de l'appuis sur le bouton dédie
		this.setDefaultCloseOperation(Jframe.EXIT_ON_CLOSE);

	
	}

		




}

