package programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils;

import lombok.Data;
import lombok.AllArgsConstructor;
@AllArgsConstructor
@Data
public class PersonInfo {
    private String firstName;
    private String lastName;
    private String patronymic;
    private byte[] planOfHouse;
    private byte[] document;
}
