/**
 * Контроллер, который отвечает за окно с лабораторными работами.
 * Не совсем хорошо написан, можно было использовать паттерн наблюдатель, но я не хочу исправлять сильно.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.laboratories;

import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.AnchorPane;
import programmingLanguagesJava.laboratories.ConsoleReader;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;
import programmingLanguagesJava.laboratories.GUI.config.JsonSimpleParser;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;

import java.net.URL;
import java.util.Optional;
import java.util.ResourceBundle;
import java.util.stream.Stream;

public class Laboratories extends BaseController {

    @FXML private Button clearInput, startQuestion;
    @FXML private Button zeroButton, firstButton, firstDotFirstButton, secondButton, thirdButton, thirdDotFirstButton, fourthButton;
    @FXML private Label openSlider, closeSlider;
    @FXML private AnchorPane slider;
    @FXML private ComboBox<String> combobox;
    @FXML private TextArea condition, output;
    @FXML private TextField inputArgs;

    private String buttonText;
    private final ComboboxConfigurator comboboxConfigurator = new ComboboxConfigurator();
    private final JsonSimpleParser data = JsonSimpleParser.getInstance();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        comboboxConfigurator.defaultConfiguration(combobox);

        // Контроллер, который отвечает за боковой слайдер меню
        new SliderController(slider, openSlider, closeSlider).sliderEvent();

        // Связывание кнопок
        setupButtonLabsEvent();
        setupClearInputButton();
        setupStartQuestionButton();


        combobox.valueProperty().addListener((obs, oldVal, newVal) -> Optional.ofNullable(newVal)
                .ifPresent(value -> condition.setText(data.get(buttonText, value))));

    }

    /**
     * Метод, который отвечает за связывание кнопок лабораторных работ с combobox
     */
    private void setupButtonLabsEvent() {
        Stream.of(
                zeroButton,
                firstButton,
                firstDotFirstButton,
                secondButton,
                thirdButton,
                thirdDotFirstButton,
                fourthButton
                ).forEach(this::setupButton);
    }

    /**
     * Настройка отдельной кнопки
     * @param button кнопка, которую мы хотим настроить
     */
    private void setupButton(Button button) {
        buttonConfigurator.setupButtonEvent(button, event -> {
            buttonText = button.getText();
            comboboxConfigurator.setupComboboxEvent(combobox, button);
        });
    }

    /**
     * Метод, который отвечает за обработку кнопок с очисткой данных, запуском методов
     */
    private void setupClearInputButton() {
        buttonConfigurator.setupButtonEvent(clearInput, event -> {
            condition.clear();
            inputArgs.clear();
            output.clear();
        });
    }

    /**
     * Метод, который настраивает запуск обработки заданий при выбранных значениях у combobox и кнопки
     */
    private void setupStartQuestionButton() {
        buttonConfigurator.setupButtonEvent(startQuestion, event -> {
            var value = combobox.getValue();
            if (value != null) {
                var classLaboratory = comboboxConfigurator.getKeyButton(buttonText);
                var inputData = inputArgs.getText();
                var comboboxData = value.split("\\s+")[0];
                output.setText((String) ConsoleReader.executeTask(classLaboratory, comboboxData, inputData));
            }
        });
    }


}
