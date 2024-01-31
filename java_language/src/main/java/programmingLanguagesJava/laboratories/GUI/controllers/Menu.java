/*
 * Данный модуль описывает контроллеры (обработчики событий для Меню)
 * Здесь определены действия для кнопок, часов, плеера (звук при наведении на кнопки)
 */

package programmingLanguagesJava.laboratories.GUI.controllers;


import javafx.animation.AnimationTimer;
import javafx.animation.PauseTransition;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.input.MouseEvent;
import javafx.scene.text.Text;
import javafx.scene.media.AudioClip;
import javafx.util.Duration;

import java.io.IOException;
import java.net.URL;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Objects;
import java.util.ResourceBundle;

public class Menu implements Initializable {

    @FXML
    private Button exitButton;

    @FXML
    private Button ButtonLabs;

    @FXML
    private Button ButtonProject;

    @FXML
    private Text minutesTimer;

    @FXML
    private Text secondsTimer;

    @FXML
    private Text hourTimer;

    // AudioClip лучше, чем Media, так как подходит для коротких звуков, вручную перематывать не нужно.
    private final AudioClip audioClipHover = new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toExternalForm());
    private final AudioClip audioClipClick = new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toExternalForm());

    private final SceneController controller = new SceneController();

    /**
     * Здесь вот точка запуска программы контроллеров происходит. Параметрами я даже не пользуюсь, но они нужны.
     */
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        clock();

        setupButtonEvent(ButtonLabs, event -> {

            try {
                controller.switchFromMenuToLaboratories(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

        setupButtonEvent(ButtonProject, event -> {
            try {
                controller.switchFromMenuToProject(event);
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

    private void setupButtonEvent(Button button, EventHandler<MouseEvent> eventHandler) {
        button.setOnMouseEntered(event -> {
            new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toString()).play();
        });

        button.setOnMouseClicked(event -> {
            new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toString()).play();
            eventHandler.handle(event); // Передача объекта MouseEvent в обработчике события
        });
    }


    /**
     * Контроллер для часов.
     * Все изменения в UI нужно делать в одном потоке по правилам JavaFx.
     * Здесь создается анонимный класс, который определяет наши часы.
     */
    private void clock() {
        var timer = new AnimationTimer() {
            @Override
            public void handle(long now) {
                Platform.runLater(() -> {
                    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");
                    hourTimer.setText(LocalDateTime.now().format(formatter).substring(0, 2));
                    minutesTimer.setText(LocalDateTime.now().format(formatter).substring(3, 5));
                    secondsTimer.setText(LocalDateTime.now().format(formatter).substring(6, 8));
                });
            }
        };
        timer.start();
    }
}
