/**
 * Контроллер, который отвечает за окно с лабораторными работами.
 */


package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.animation.*;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.layout.AnchorPane;
import javafx.util.Duration;
import programmingLanguagesJava.laboratories.ConsoleReader;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;
import programmingLanguagesJava.laboratories.GUI.config.JsonSimpleParser;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public class Laboratories implements Initializable {

    @FXML private Button backButton, exitButton, clearInput, startQuestion;
    @FXML private Button zeroButton, firstButton, firstDotFirstButton, secondButton, thirdButton, thirdDotFirstButton, fourthButton;
    @FXML private Label openSlider, closeSlider;
    @FXML private AnchorPane slider;
    @FXML private ComboBox<String> combobox;
    @FXML private TextArea condition, output;
    @FXML private TextField inputArgs;

    private String buttonText;
    private final SceneController controller = new SceneController();
    private final ButtonConfigurator buttonConfigurator = new ButtonConfigurator();
    private final ComboboxConfigurator comboboxConfigurator = new ComboboxConfigurator();
    private final JsonSimpleParser data = new JsonSimpleParser();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        new SliderController(slider, openSlider, closeSlider).sliderEvent();

        buttonLabsEvent();
        buttonEvent();

        comboboxConfigurator.defaultConfiguration(combobox);

        combobox.valueProperty().addListener((obs, oldVal, newVal) -> {

            if (newVal != null)
                condition.setText(data.get(buttonText, newVal));

        });

    }

    private void buttonLabsEvent() {

        Button[] allButtons = {
                zeroButton, firstButton, firstDotFirstButton,
                secondButton, thirdButton, thirdDotFirstButton, fourthButton
        };

        for (var button : allButtons) {
            buttonConfigurator.setupButtonEvent(button, event -> {

                buttonText = button.getText();
                comboboxConfigurator.setupComboboxEvent(combobox, button);

            });
        }

    }


    private void buttonEvent() {

        buttonConfigurator.setupButtonEvent(backButton, event -> {

            try {
                controller.switchToMenu(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

        buttonConfigurator.setupButtonEvent(exitButton, event -> {

            PauseTransition pause = new PauseTransition(Duration.millis(100));
            pause.setOnFinished(evt -> Platform.exit());
            pause.play();

        });


        buttonConfigurator.setupButtonEvent(clearInput, event -> {
            condition.clear();
            inputArgs.clear();
            output.clear();
        });


        buttonConfigurator.setupButtonEvent(startQuestion, event1 -> {
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
