package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.addingNames;

import javafx.scene.control.TextField;

import java.util.HashSet;

public class TextFieldAddController {

    private final TextField textField;

    private final HashSet<String> persons = new HashSet<>();

    public TextFieldAddController(TextField textField) {
        this.textField = textField;
    }

    public HashSet<String> event() {
        persons.add(textField.getText());
        textField.clear();
        return persons;
    }

}
