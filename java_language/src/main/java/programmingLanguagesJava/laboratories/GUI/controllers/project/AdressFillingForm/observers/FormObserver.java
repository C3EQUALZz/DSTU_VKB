/**
 * Здесь используется паттерн программирования - наблюдатель.
 * В моем случае данный класс отвечает за то, чтобы все телодвижения от пользователя отслеживались для включения кнопки
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.observers;

import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.project.Observer;

import java.util.List;

@RequiredArgsConstructor
public class FormObserver implements Observer {
    private final TextField textField;
    private final ComboBox<String> comboBox;
    private final List<Button> buttons;

    /**
     * Метод, который запускает слушателя
     */
    @Override
    public void listen() {
        textField.textProperty().addListener((observable, oldValue, newValue) -> checkFields());
        comboBox.getSelectionModel().selectedItemProperty().addListener((observable, oldValue, newValue) -> checkFields());
    }

    /**
     * Здесь происходит проверка на пустоту полей. Если же они пустые, то кнопка отключается, а в ином случае работает
     */
    private void checkFields() {

        var allFilled = !textField.getText().isEmpty() &&
                comboBox.getValue() != null &&
                !comboBox.getValue().isEmpty();

        buttons.forEach(button -> button.setDisable(!allFilled));

    }
}
