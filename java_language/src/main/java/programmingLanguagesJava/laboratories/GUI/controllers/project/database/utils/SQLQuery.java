package programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils;

public enum SQLQuery {
    ;
    public static final String INSERT_REMAINING = "INSERT INTO Remaining_info (document, plan_of_house) VALUES (?, ?)";
    public static final String INSERT_HUMAN = "INSERT INTO Peoples (last_name, first_name, patronymic, post, remaining_info) VALUES (?, ?, ?, ?, ?)";
    public static final String MAX_ID = "SELECT MAX(id) FROM Remaining_info";
}
