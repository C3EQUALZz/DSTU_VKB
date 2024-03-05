package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.addingNames;

import javafx.animation.TranslateTransition;
import javafx.scene.control.TextField;
import javafx.util.Duration;

import java.util.LinkedList;

public class TextFieldAddController {

    private final TextField textField;
    private final TranslateTransition transition;

    private final LinkedList<String> persons = new LinkedList<>();

    public TextFieldAddController(TextField textField) {
        this.textField = textField;
        this.transition = new TranslateTransition(Duration.seconds(0.1), textField);
    }

    public void event() {
        persons.add(textField.getText());
        transition.setToX(400); // Устанавливаем конечную позицию по оси X
        transition.setOnFinished(event -> textField.clear()); // Очищаем текст после завершения анимации
    }

    @SuppressWarnings("unused")
    public LinkedList<String> getPersons() {
        return persons;
    }

    @SuppressWarnings("unused")
    public void clearPersons() {
        persons.clear();
    }




}
