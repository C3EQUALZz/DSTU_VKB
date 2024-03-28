package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DataBaseSQLite implements DAO {
    private static final String DATABASE_URL = String.format(
            "jdbc:sqlite:%s%s",
            System.getProperty("user.dir"),
            "java_language/src/main/resources/projectFiles/data/security_information_db.db");
    private static DataBaseSQLite instance;
    private Connection connection;

    private DataBaseSQLite() {
        try {
            connection = DriverManager.getConnection(DATABASE_URL);
        } catch (SQLException e) {
            throw new RuntimeException("Не получилось подключиться к базе данных", e);
        }
    }

    public static synchronized DataBaseSQLite getInstance() {
        if (instance == null) {
            instance = new DataBaseSQLite();
        }

        return instance;
    }

    @Override
    public void addAddress(String address) {

    }

    @Override
    public void addFullName(String fullName) {

    }

    @Override
    public void addMainPerson(String person) {

    }

    @Override
    public void addBuildingPlan(String pathToBuildingPlan) {

    }

    @Override
    public void addAllResponsiblePeople(String persons) {

    }

    @Override
    public void addContractDocument(String pathToDocument) {

    }

    @Override
    public String getAddress() {
        return null;
    }

    @Override
    public String getFullName() {
        return null;
    }

    @Override
    public String getMainPerson() {
        return null;
    }

    @Override
    public String getBuildingPlan() {
        return null;
    }

    @Override
    public String getAllResponsiblePeople() {
        return null;
    }

    @Override
    public String getContractDocument() {
        return null;
    }
}
