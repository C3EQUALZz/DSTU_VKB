package programmingLanguagesJava.lections.seventhLection;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    public static void main(String[] args) {
        Connection connection = null;

        try {
            connection = DriverManager.getConnection("jdbc:sqlite:java_language/src/main/java/programmingLanguagesJava/lections/seventhLection/database.sqlite");

            if (connection != null) {
                System.out.println("Подключилися к БД");
            }


        } catch (SQLException e) {
            System.out.println(e.getClass().getName() + ":" + e.getMessage());
            System.out.println("Error en la connection");
        }
    }
}
