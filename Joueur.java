package ClasseMétier;

import java.util.ArrayList;

public class Joueur {
	
	//Attribut
	private int id;
	private String identifiant;
	private String motDePasse;
	private int monnaie;
	private static ArrayList<Joueur> listeJoueur ;
	
	
	public Joueur(String nom, String mdp) {
		listeJoueur.add(this);
		this.id=listeJoueur.size();
		this.identifiant = nom;
		this.motDePasse = mdp;
		this.monnaie = 0;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getIdentifiant() {
		return identifiant;
	}

	public void setIdentifiant(String identifiant) {
		this.identifiant = identifiant;
	}

	public String getMotDePasse() {
		return motDePasse;
	}

	public void setMotDePasse(String motDePasse) {
		this.motDePasse = motDePasse;
	}

	public int getMonnaie() {
		return monnaie;
	}

	public void setMonnaie(int monnaie) {
		this.monnaie = monnaie;
	}

	public static ArrayList<Joueur> getListeJoueur() {
		return listeJoueur;
	}

	public static void setListeJoueur(ArrayList<Joueur> listeJoueur) {
		Joueur.listeJoueur = listeJoueur;
	}
	
	
}
