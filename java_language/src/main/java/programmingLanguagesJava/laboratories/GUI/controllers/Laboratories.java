package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.animation.PauseTransition;
import javafx.animation.TranslateTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import javafx.scene.media.AudioClip;
import javafx.util.Duration;

import java.io.IOException;
import java.net.URL;
import java.util.Objects;
import java.util.ResourceBundle;

public class Laboratories implements Initializable {
    @FXML
    private Button backButton;

    @FXML
    private Label closeSlider;

    @FXML
    private Button exitButton;

    @FXML
    private Label openSlider;

    @FXML
    private AnchorPane slider;

    private final AudioClip audioClipHover = new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toExternalForm());
    private final AudioClip audioClipClick = new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toExternalForm());
    private final SceneController controller = new SceneController();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        buttonToMenuEvent();
        buttonExitEvent();
        menuEvent();
    }

    private void buttonToMenuEvent() {
        backButton.setOnMouseEntered(event -> audioClipHover.play());

        backButton.setOnMouseClicked(event -> {
            audioClipClick.play();

            try {
                controller.switchToMenu(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
    }

    private void buttonExitEvent() {

        exitButton.setOnMouseEntered(event -> audioClipHover.play());

        exitButton.setOnMouseClicked(event -> {
            audioClipClick.play();

            PauseTransition pause = new PauseTransition(Duration.millis(100));
            pause.setOnFinished(evt -> Platform.exit());
            pause.play();
        });

    }

    private void menuEvent() {

        openSlider.setOnMouseClicked(event -> {
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


        closeSlider.setOnMouseClicked(event -> {
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

}
