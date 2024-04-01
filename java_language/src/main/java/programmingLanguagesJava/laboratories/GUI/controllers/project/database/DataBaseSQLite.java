package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.Person;

import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.HashMap;

/**
 * Класс DataBaseSQLite предоставляет методы для взаимодействия с базой данных SQLite.
 * Он использует DAO (Data Access Object) для работы с таблицами Peoples и Remaining_info.
 */
public class DataBaseSQLite {

    private static final String DATABASE_URL = String.format(
            "jdbc:sqlite:%s%s",
            System.getProperty("user.dir"),
            "/src/main/resources/projectFiles/data/security_information_db.db"
    );

    private final RemainingInfoDAO remainingInfoDAO;
    private final PeoplesDAO peoplesDAO;
    private static DataBaseSQLite instance;

    /**
     * Конструктор класса DataBaseSQLite.
     * Он устанавливает соединение с базой данных и инициализирует DAO для таблиц Peoples и Remaining_info.
     *
     * @throws RuntimeException Если не удалось подключиться к базе данных.
     */
    private DataBaseSQLite() {

        try {

            var connection = DriverManager.getConnection(DATABASE_URL);
            remainingInfoDAO = new RemainingInfoDAO(connection);
            peoplesDAO = new PeoplesDAO(connection);

        } catch (SQLException e) {

            throw new RuntimeException("Не получилось подключиться к базе данных", e);

        }
    }

    /**
     * Метод getInstance() возвращает единственный экземпляр класса DataBaseSQLite (Singleton pattern).
     *
     * @return Единственный экземпляр класса DataBaseSQLite.
     */
    public static synchronized DataBaseSQLite getInstance() {

        if (instance == null) {
            instance = new DataBaseSQLite();
        }

        return instance;
    }

    /**
     * Метод insert() вставляет данные о человеке в базу данных.
     * Он использует DAO для вставки данных в таблицы Peoples и Remaining_info.
     *
     * @param personData Данные о человеке в формате HashMap.
     */
    public void insert(HashMap<String, String> personData) {
        remainingInfoDAO.insert(personData.get("pathToFile"), personData.get("buildingPlan"));
        var remainingInfoId = remainingInfoDAO.getLastIndex();
        var listOfPersons = Person.createPeoples(personData.get("allPeople"), personData.get("mainPerson"));
        peoplesDAO.insert(listOfPersons, remainingInfoId);
    }

}
