package ClasseDAO;

import java.sql.Connection;
import java.sql.SQLException;
import com.mysql.cj.jdbc.MysqlDataSource;

public class SingleConnection {
    private static Connection connect ;
	
	private SingleConnection( String dbName, String login, String password) {
		String url="jdbc:mysql://localhost:3306/"+dbName+"?serverTimezone=UTC";
		MysqlDataSource mysqlDS = new MysqlDataSource();
		mysqlDS.setURL(url);
		mysqlDS.setUser(login);
		mysqlDS.setPassword(password);
	}
	
	public static Connection getInstance(String dbName, String login, String password){
		if(connect == null){
			new SingleConnection(dbName, login, password);
			} 
		return connect;   
	}
	
	public void close(Connection con) {
		try {
			con.close();
		} catch (SQLException e) {
			System.err.println("Erreur de parcours de déconnexion");
			e.printStackTrace();
		}
	}
}
