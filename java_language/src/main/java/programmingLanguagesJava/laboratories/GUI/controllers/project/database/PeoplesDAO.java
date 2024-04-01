package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.Person;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.SQLQuery;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

public class PeoplesDAO {
    private final Connection connection;

    public PeoplesDAO(Connection connection) {
        this.connection = connection;
    }

    public void insert(List<Person> people, int remainingInfoId) {

        try (var preparedStatement = connection.prepareStatement(SQLQuery.INSERT_HUMAN)) {

            for (Person person : people) {

                preparedStatement.setString(1, person.getSecondName());
                preparedStatement.setString(2, person.getFirstName());
                preparedStatement.setString(3, person.getPatronymic());
                preparedStatement.setInt(4, person.getPost());
                preparedStatement.setInt(5, remainingInfoId);

                preparedStatement.addBatch();
            }

            preparedStatement.executeBatch();

        } catch (SQLException e) {
            throw new RuntimeException("Ошибка при добавлении людей в базу данных", e);
        }
    }

}
