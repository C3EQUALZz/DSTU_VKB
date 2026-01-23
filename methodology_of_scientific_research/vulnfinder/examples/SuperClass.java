import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class SuperClass {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.out.println("Usage: SuperClass <username>");
            return;
        }

        String user = args[0];
        String url = "jdbc:sqlite:app.db";

        try (Connection conn = DriverManager.getConnection(url);
             Statement stmt = conn.createStatement()) {
            String query = "SELECT * FROM users WHERE name = '" + user + "'";
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                System.out.println(rs.getString("name"));
            }
        }
    }
}

