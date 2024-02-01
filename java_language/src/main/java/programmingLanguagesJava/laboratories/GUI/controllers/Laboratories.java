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
import programmingLanguagesJava.laboratories.GUI.Config.Configurator;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public class Laboratories implements Initializable {

    @FXML
    private Button zeroButton, firstButton, firstDotFirstButton, secondButton, thirdButton, thirdDotFirstButton, fourthButton;

    @FXML
    private Button backButton, exitButton;

    @FXML
    private Label openSlider, closeSlider;

    @FXML
    private AnchorPane slider;

    @FXML
    private ComboBox<String> combobox;

    private final SceneController controller = new SceneController();
    private final Configurator configurator = new Configurator();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        menuEvent();
        comboboxEvent();
        buttonsEvent();

        configurator.setupButtonEvent(backButton, event -> {

            try {
                controller.switchToMenu(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

        configurator.setupButtonEvent(exitButton, event -> {

            PauseTransition pause = new PauseTransition(Duration.millis(100));
            pause.setOnFinished(evt -> Platform.exit());
            pause.play();

        });


    }

    /**
     * Настройка slider меню, которое движется справа.
     * Есть баг, что в начале почему-то сверху находится closeSlider, а не openSlider.
     * В общем, поэтому с самого начала меню закрыто, а не открыто.
     * Здесь под капотом, если что 2 кнопки, которые совпадают 1 в 1.
     */
    private void menuEvent() {

        // Состояние закрытого меню
        slider.setTranslateX(-500);

        // Установка звука на тот момент, когда мы наводимся на кнопку меню.
        openSlider.setOnMouseEntered(event -> configurator.hoverClip.play());

        // Установка звука на тот момент, когда мы нажимаем кнопку.
        openSlider.setOnMouseClicked(event -> {

            configurator.clickClip.play();
            // Са
            TranslateTransition slide = new TranslateTransition();
            slide.setDuration(Duration.seconds(0.4));
            slide.setNode(slider);

            slide.setToX(0);
            slide.play();

            slider.setTranslateX(-500);

            slide.setOnFinished(actionEvent -> {
                openSlider.setVisible(false);
                closeSlider.setVisible(true);
            });
        });

        closeSlider.setOnMouseEntered(event -> configurator.hoverClip.play());

        closeSlider.setOnMouseClicked(event -> {
            configurator.clickClip.play();

            TranslateTransition slide = new TranslateTransition();
            slide.setDuration(Duration.seconds(0.4));
            slide.setNode(slider);

            slide.setToX(-500);
            slide.play();

            slider.setTranslateX(0);

            slide.setOnFinished(actionEvent -> {
                openSlider.setVisible(true);
                closeSlider.setVisible(false);
            });
        });
    }

    private void comboboxEvent() {
        combobox.setOnMouseEntered(event -> configurator.hoverClip.play());

        combobox.setOnMouseClicked(event -> configurator.clickClip.play());

        combobox.setCellFactory(param -> new ListCell<>() {
            @Override
            protected void updateItem(String item, boolean empty) {
                super.updateItem(item, empty);
                if (empty || item == null) {
                    setText(null);
                } else {
                    setText(item);
                    setOnMouseEntered(event -> configurator.hoverClip.play());
                    setOnMouseClicked(event -> configurator.clickClip.play());
                }
            }
        });
        combobox.setDisable(true);
    }

    private void buttonsEvent() {

        configurator.setupButtonEvent(zeroButton, event -> {
            combobox.setDisable(false);
            combobox.getItems().clear();

            String[] questions = {"1 задание", "2 задание", "3 задание", "4 задание", "5 задание", "6 задание"};
            combobox.getItems().addAll(questions);
        });

        configurator.setupButtonEvent(firstButton, event -> {
            combobox.setDisable(true);
            combobox.getItems().clear();

            String[] questions = {"1 задание", "2 задание", "3 задание", "4 задание", "5 задание"};
            combobox.getItems().addAll(questions);
        });

        configurator.setupButtonEvent(firstDotFirstButton, event -> {

        });

        configurator.setupButtonEvent(secondButton, event -> {

        });

        configurator.setupButtonEvent(thirdButton, event -> {

        });

        configurator.setupButtonEvent(thirdDotFirstButton, event -> {

        });

        configurator.setupButtonEvent(fourthButton, event -> {

        });


    }
}
