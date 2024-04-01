/**
 * Класс, который опять-таки реализует паттерн DAO
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.OptionalInt;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.FileUtil;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.SQLQuery;

/**
 * Класс RemainingInfoDAO предоставляет методы для взаимодействия с таблицей Remaining_info в базе данных.
 */
public class RemainingInfoDAO {
    private final Connection connection;

    /**
     * Конструктор класса RemainingInfoDAO.
     *
     * @param connection Объект Connection, представляющий соединение с базой данных.
     */
    public RemainingInfoDAO(Connection connection) {
        this.connection = connection;
    }

    /**
     * Метод insert() вставляет данные в таблицу Remaining_info в базе данных.
     *
     * @param pathToFile Путь к файлу, который нужно вставить в таблицу.
     * @param buildingPlan План здания, который нужно вставить в таблицу.
     * @throws RuntimeException Если произошла ошибка при вставке данных в базу данных.
     */
    public void insert(String pathToFile, String buildingPlan) {
        try (var preparedStatement = connection.prepareStatement(SQLQuery.INSERT_REMAINING)) {

            preparedStatement.setBytes(1, FileUtil.readBytesFromFile(pathToFile));
            preparedStatement.setBytes(2, FileUtil.readBytesFromFile(buildingPlan));
            preparedStatement.executeUpdate();

        } catch (SQLException e) {
            throw new RuntimeException("Ошибка при вставке данных в таблицу Remaining_info", e);
        }
    }

    /**
     * Метод getLastIndex() возвращает последний индекс из таблицы Remaining_info.
     *
     * @return Последний индекс из таблицы Remaining_info.
     * @throws RuntimeException Если произошла ошибка при получении последнего индекса из базы данных.
     */
    public int getLastIndex() {
        try (var resultSet = connection.createStatement().executeQuery(SQLQuery.MAX_ID)) {

            return OptionalInt.of(resultSet.getInt(1)).orElse(0);

        } catch (SQLException e) {

            throw new RuntimeException("Ошибка при получении последнего индекса из таблицы Remaining_info", e);

        }
    }
}
