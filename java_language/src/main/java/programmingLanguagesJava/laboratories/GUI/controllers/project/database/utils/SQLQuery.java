/**
 * Здесь у меня перечисление для удобства.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils;

/**
 * Здесь содержаться готовые SQL запросы, которые я буду использовать.
 * Мне так больше нравится, чем писать запросы прямо в коде.
 * ORM не хочу делать, так как гемор
 */
public enum SQLQuery {
    ;
    // Вставка в таблицу Remaining_info
    public static final String INSERT_REMAINING = "INSERT INTO Remaining_info (document, plan_of_house) VALUES (?, ?)";
    // Вставка в таблицу Peoples
    public static final String INSERT_HUMAN = "INSERT INTO Peoples (last_name, first_name, patronymic, post, remaining_info) VALUES (?, ?, ?, ?, ?)";
    // Поиск максимального индекса в базе данных
    public static final String MAX_ID = "SELECT MAX(id) FROM Remaining_info";

    public static final String JOIN_TABLES = """
            SELECT Peoples.first_name,
                   Peoples.last_name,
                   Peoples.patronymic,
                   Remaining_info.plan_of_house,
                   Remaining_info.document

            FROM Peoples

            JOIN Remaining_info ON Peoples.remaining_info = Remaining_info.id

            """;
}
