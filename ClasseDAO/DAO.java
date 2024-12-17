package ClasseDAO;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public abstract class DAO<T> {
    //Attributs
	protected static Connection connect;
	protected Statement stmt;
	
	//méthodes
	public abstract T create(T objet);
	public abstract T update(T object);
	public abstract void delete(T object);
	
	public void open() {
		connect = SingleConnection.getInstance("absences", "java","JeSappelleGroot");
	}
	
	public void close() {
		try {
			connect.close();
		} catch (SQLException e) {
			System.err.println("Erreur lors de la déconnexion");
			e.printStackTrace();
		}
	}

}
