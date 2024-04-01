package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.Person;

import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.HashMap;

public class DataBaseSQLite {

    private static final String DATABASE_URL = String.format(
            "jdbc:sqlite:%s%s",
            System.getProperty("user.dir"),
            "/src/main/resources/projectFiles/data/security_information_db.db"
    );

    private final RemainingInfoDAO remainingInfoDAO;
    private final PeoplesDAO peoplesDAO;
    private static DataBaseSQLite instance;


    private DataBaseSQLite() {

        try {

            var connection = DriverManager.getConnection(DATABASE_URL);
            remainingInfoDAO = new RemainingInfoDAO(connection);
            peoplesDAO = new PeoplesDAO(connection);

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

    public void insert(HashMap<String, String> personData) {
        remainingInfoDAO.insert(personData.get("pathToFile"), personData.get("buildingPlan"));
        int remainingInfoId = remainingInfoDAO.getLastIndex();
        var listOfPersons = Person.createPeoples(personData.get("allPeople"), personData.get("mainPerson"));
        peoplesDAO.insert(listOfPersons, remainingInfoId);
    }

}
