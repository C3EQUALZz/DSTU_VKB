/**
 * Здесь реализуется паттерн DAO для базы данных
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.database;

import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.Person;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.SQLQuery;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

/**
 * Класс PeoplesDAO предоставляет методы для взаимодействия с таблицей Peoples в базе данных.
 */
@RequiredArgsConstructor
public class PeoplesDAO {
    private final Connection connection;


    /**
     * Метод insert() вставляет список людей в таблицу Peoples в базе данных.
     *
     * @param people          Список объектов Person, представляющих людей, которых нужно вставить в таблицу.
     * @param remainingInfoId ID информации, оставшейся для этих людей.
     * @throws RuntimeException Если произошла ошибка при вставке людей в базу данных.
     */
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
