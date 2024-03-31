/**
 * Здесь реализован паттерн слушатель, который в зависимости от значения полей включает кнопку
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.observers;

import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.controllers.project.Observer;

public class TextFieldsObserver implements Observer {
    private final TextField loginField;
    private final PasswordField passwordField;
    private final Button button;

    public TextFieldsObserver(TextField loginField, PasswordField passwordField, Button button) {
        this.loginField = loginField;
        this.passwordField = passwordField;
        this.button = button;
        listen();
    }

    /**
     * Метод, который запускает слушателя для нашего класса
     */
    @Override
    public void listen() {
        loginField.textProperty().addListener((observable, oldValue, newValue) -> checkFields());
        passwordField.textProperty().addListener((observable, oldValue, newValue) -> checkFields());
    }

    /**
     * Метод, который проверяет равенство поля. Здесь можно сделать дополнительную логику в БД
     */
    private void checkFields() {
        var allFilled = !loginField.getText().isEmpty() && !passwordField.getText().isEmpty();
        button.setDisable(!allFilled);
    }

}
