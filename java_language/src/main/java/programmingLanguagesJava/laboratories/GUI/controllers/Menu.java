/*
 * Данный модуль описывает контроллеры (обработчики событий для Меню)
 * Здесь определены действия для кнопок, часов, плеера (звук при наведении на кнопки)
 */

package programmingLanguagesJava.laboratories.GUI.controllers;


import javafx.animation.AnimationTimer;
import javafx.animation.PauseTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.text.Text;
import javafx.scene.media.AudioClip;
import javafx.util.Duration;

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

    /**
     * Здесь вот точка запуска программы контроллеров происходит. Параметрами я даже не пользуюсь, но они нужны.
     */
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        clock();
        buttonLabsEvent();
        buttonProjectEvent();
        exitEvent();
    }

    /**
     * Метод, который является обработчиком событий для кнопки с лабораторными работами
     */
    private void buttonLabsEvent() {
        // Установление обработчика событий для ButtonLabs, который будет воспроизводить аудиофайл при наведении мыши
        ButtonLabs.setOnMouseEntered(event -> audioClipHover.play());

        ButtonLabs.setOnMouseClicked(event -> {
            audioClipClick.play();
        });
    }

    /**
     * Метод, который является обработчиком событий для кнопки с проектом
     */
    private void buttonProjectEvent() {
        ButtonProject.setOnMouseEntered(event -> audioClipHover.play());

        ButtonProject.setOnMouseClicked(event -> {
            audioClipClick.play();
        });

    }

    private void exitEvent() {
        exitButton.setOnMouseEntered(event -> audioClipHover.play());

        exitButton.setOnMouseClicked(event -> {
            audioClipClick.play();

            PauseTransition pause = new PauseTransition(Duration.millis(100));
            pause.setOnFinished(evt -> Platform.exit());
            pause.play();
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
