/**
 * Контроллер, который отвечает за окно с лабораторными работами.
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
import java.util.ResourceBundle;

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
    private final JsonSimpleParser data = new JsonSimpleParser();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        super.initialize(url, resourceBundle);

        // Контроллер, который отвечает за боковой слайдер меню
        new SliderController(slider, openSlider, closeSlider).sliderEvent();

        // Связывание кнопок на слайдере с combobox
        buttonLabsEvent();

        buttonEvent();

        comboboxConfigurator.defaultConfiguration(combobox);

        combobox.valueProperty().addListener((obs, oldVal, newVal) -> {

            if (newVal != null)
                condition.setText(data.get(buttonText, newVal));

        });

    }

    /**
     * Метод, который отвечает за связывание кнопок лабораторных работ с combobox
     */
    private void buttonLabsEvent() {

        // Все лабораторные в качестве кнопок
        Button[] allButtons = {
                zeroButton, firstButton, firstDotFirstButton,
                secondButton, thirdButton, thirdDotFirstButton, fourthButton
        };

        for (var button : allButtons) {
            buttonConfigurator.setupButtonEvent(button, event -> {

                // С помощью текста с кнопки я распознаю количество заданий в лабораторной
                buttonText = button.getText();
                comboboxConfigurator.setupComboboxEvent(combobox, button);

            });
        }

    }

    // Метод, который отвечает за обработку кнопок с очисткой данных, запуском методов
    private void buttonEvent() {
        // Настраиваю так, что при нажатии на "очистить данные" убираются все данные
        buttonConfigurator.setupButtonEvent(clearInput, event -> {
            condition.clear();
            inputArgs.clear();
            output.clear();
        });


        buttonConfigurator.setupButtonEvent(startQuestion, event1 -> {
            var value = combobox.getValue();

            // combobox может принимать значение null, а парсеру не нравятся такие значения.
            if (value != null) {
                var classLaboratory = comboboxConfigurator.getKeyButton(buttonText);
                var inputData = inputArgs.getText();
                var comboboxData = value.split("\\s+")[0];

                output.setText((String) ConsoleReader.executeTask(classLaboratory, comboboxData, inputData));
            }
        });

    }


}
