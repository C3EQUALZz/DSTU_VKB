package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.animation.PauseTransition;
import javafx.animation.TranslateTransition;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.media.AudioClip;
import javafx.util.Duration;

import java.io.IOException;
import java.net.URL;
import java.util.Objects;
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

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        menuEvent();
        buttonsEvent();

        setupButtonEvent(backButton, event -> {

            try {
                controller.switchToMenu(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

        setupButtonEvent(exitButton, event -> {

            PauseTransition pause = new PauseTransition(Duration.millis(100));
            pause.setOnFinished(evt -> Platform.exit());
            pause.play();

        });


    }

    private void menuEvent() {

        slider.setTranslateX(-1000);

        openSlider.setOnMouseEntered(event -> new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toExternalForm()).play());

        openSlider.setOnMouseClicked(event -> {
            new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toExternalForm()).play();

            TranslateTransition slide = new TranslateTransition();
             slide.setDuration(Duration.seconds(0.4));
             slide.setNode(slider);

             slide.setToX(0);
             slide.play();

            slider.setTranslateX(-1000);

            slide.setOnFinished(actionEvent -> {
                openSlider.setVisible(false);
                closeSlider.setVisible(true);
            });
        });

        closeSlider.setOnMouseEntered(event -> new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toExternalForm()).play());

        closeSlider.setOnMouseClicked(event -> {
            new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toExternalForm()).play();

            TranslateTransition slide = new TranslateTransition();
            slide.setDuration(Duration.seconds(0.4));
            slide.setNode(slider);

            slide.setToX(-1000);
            slide.play();

            slider.setTranslateX(0);

            slide.setOnFinished(actionEvent -> {
                openSlider.setVisible(true);
                closeSlider.setVisible(false);
            });
        });
    }

    private void buttonsEvent() {

        setupButtonEvent(zeroButton, event -> {
            combobox.getItems().clear();

            String[] questions = {"1 задание", "2 задание", "3 задание", "4 задание", "5 задание", "6 задание"};
            combobox.getItems().addAll(questions);
        });

        setupButtonEvent(firstButton, event -> {
            combobox.getItems().clear();

            String[] questions = {"1 задание", "2 задание", "3 задание", "4 задание", "5 задание"};
            combobox.getItems().addAll(questions);
        });

        setupButtonEvent(firstDotFirstButton, event -> {

        });

        setupButtonEvent(secondButton, event -> {

        });

        setupButtonEvent(thirdButton, event -> {

        });

        setupButtonEvent(thirdDotFirstButton, event -> {

        });

        setupButtonEvent(fourthButton, event -> {

        });


    }

    /**
     * Настройка кнопки с определенными параметрами.
     *
     * @param button       кнопка, на которую мы хотим назначить настройку по нажатию и т.п.
     * @param eventHandler событие, которое мы хотим обработать.
     */
    private void setupButtonEvent(Button button, EventHandler<MouseEvent> eventHandler) {
        // Обработка того момента, когда мышка наводится на кнопку.
        button.setOnMouseEntered(event -> {
            new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toString()).play();
        });

        button.setOnMouseClicked(event -> {
            new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toString()).play();
            eventHandler.handle(event); // Передача объекта MouseEvent в обработчике события
        });
    }


}
