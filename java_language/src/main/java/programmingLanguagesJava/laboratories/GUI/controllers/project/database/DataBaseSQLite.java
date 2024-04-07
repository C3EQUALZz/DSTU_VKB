/**
 * Один из возможных классов, то есть соединение
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import lombok.Getter;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.Person;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.SQLQuery;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

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

    @Getter
    private final Connection connection;
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

            connection = DriverManager.getConnection(DATABASE_URL);
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
    public void insert(Map<String, String> personData) {
        remainingInfoDAO.insert(personData.get("pathToFile"), personData.get("buildingPlan"));
        var remainingInfoId = remainingInfoDAO.getLastIndex();
        var listOfPersons = Person.createPeoples(personData.get("allPeople"), personData.get("mainPerson"));
        peoplesDAO.insert(listOfPersons, remainingInfoId);
    }

    /**
     * Метод loadPersonInfos() загружает информацию о людях из базы данных.
     * Он выполняет SQL-запрос JOIN_TABLES, чтобы получить данные из нескольких таблиц,
     * затем создает объекты PersonInfo на основе этих данных и добавляет их в список.
     *
     * @return Список объектов PersonInfo, содержащий информацию о людях из базы данных.
     * @throws RuntimeException Если произошла ошибка при выполнении SQL-запроса или обработке результатов.
     */
    public List<PersonInfo> loadPersonInfos() {
        var personInfos = new LinkedList<PersonInfo>();

        try (var resultSet = this.connection.createStatement().executeQuery(SQLQuery.JOIN_TABLES)) {

            while (resultSet.next()) {
                var firstName = resultSet.getString("first_name");
                var lastName = resultSet.getString("last_name");
                var patronymic = resultSet.getString("patronymic");
                var planOfHouse = resultSet.getBytes("plan_of_house");
                var document = resultSet.getBytes("document");

                personInfos.add(new PersonInfo(firstName, lastName, patronymic, planOfHouse, document));
            }

        } catch (SQLException e) {
            throw new RuntimeException("Не получилось соединить данные таблиц", e);
        }

        return personInfos;
    }

}
