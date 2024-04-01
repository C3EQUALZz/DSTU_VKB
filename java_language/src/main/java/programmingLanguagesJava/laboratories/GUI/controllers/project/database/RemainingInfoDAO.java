package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.OptionalInt;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.FileUtil;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.SQLQuery;

public class RemainingInfoDAO {
    private final Connection connection;

    public RemainingInfoDAO(Connection connection) {
        this.connection = connection;
    }

    public void insert(String pathToFile, String buildingPlan) {
        try (var preparedStatement = connection.prepareStatement(SQLQuery.INSERT_REMAINING)) {

            preparedStatement.setBytes(1, FileUtil.readBytesFromFile(pathToFile));
            preparedStatement.setBytes(2, FileUtil.readBytesFromFile(buildingPlan));
            preparedStatement.executeUpdate();

        } catch (SQLException e) {
            throw new RuntimeException("Ошибка при вставке данных в таблицу Remaining_info", e);
        }
    }

    public int getLastIndex() {
        try (var resultSet = connection.createStatement().executeQuery(SQLQuery.MAX_ID)) {

            return OptionalInt.of(resultSet.getInt(1)).orElse(0);

        } catch (SQLException e) {

            throw new RuntimeException("Ошибка при получении последнего индекса из таблицы Remaining_info", e);

        }
    }
}
