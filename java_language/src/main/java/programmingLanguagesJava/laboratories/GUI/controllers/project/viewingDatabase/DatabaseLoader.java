package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.DataBaseSQLite;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.SQLQuery;

import java.sql.SQLException;
import java.util.LinkedList;
import java.util.List;

class DatabaseLoader {
    private final DataBaseSQLite dataBaseSQl = DataBaseSQLite.getInstance();
    List<PersonInfo> loadPersonInfos() {
        var personInfos = new LinkedList<PersonInfo>();

        try (var resultSet = dataBaseSQl.connection.createStatement().executeQuery(SQLQuery.JOIN_TABLES)) {

            while (resultSet.next()) {
                var firstName = resultSet.getString("first_name");
                var lastName = resultSet.getString("last_name");
                var patronymic = resultSet.getString("patronymic");
                var planOfHouse = resultSet.getString("plan_of_house");
                var document = resultSet.getString("document");

                personInfos.add(new PersonInfo(firstName, lastName, patronymic, planOfHouse, document));
            }

        } catch (SQLException e) {
            throw new RuntimeException("Не получилось соединить данные таблиц", e);
        }

        return personInfos;
    }
}
