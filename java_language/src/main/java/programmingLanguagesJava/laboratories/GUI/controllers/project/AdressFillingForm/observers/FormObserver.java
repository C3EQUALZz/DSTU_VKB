/**
 * Здесь используется паттерн программирования - наблюдатель.
 * В моем случае данный класс отвечает за то, чтобы все телодвижения от пользователя отслеживались для включения кнопки
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.observers;

import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;

import java.util.List;

public class FormObserver implements Observer {
    private final TextField textField;
    private final ComboBox<String> comboBox;
    private final List<Button> buttons;

    /**
     * В моем случае на странице есть поле, выпадающий список, которые я хочу отслеживать
     * @param textField поле ввода, которое мне нужно, чтобы смотреть не пусто ли оно
     * @param comboBox выпадающий список, который проверяю на значения
     * @param buttons кнопки, которые хотим включать и выключать
     */
    public FormObserver(TextField textField, ComboBox<String> comboBox, List<Button> buttons) {
        this.textField = textField;
        this.comboBox = comboBox;
        this.buttons = buttons;
        listen();
    }

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
