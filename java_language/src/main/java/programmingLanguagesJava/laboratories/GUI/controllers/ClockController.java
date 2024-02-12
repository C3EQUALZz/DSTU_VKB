package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.animation.AnimationTimer;
import javafx.application.Platform;
import javafx.scene.text.Text;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class ClockController {
    private final Text hourTimer;
    private final Text minutesTimer;
    private final Text secondsTimer;

    public ClockController(Text hourTimer, Text minutesTimer, Text secondsTimer) {
        this.hourTimer = hourTimer;
        this.minutesTimer = minutesTimer;
        this.secondsTimer = secondsTimer;
    }

    /**
     * Контроллер для часов.
     * Все изменения в UI нужно делать в одном потоке по правилам JavaFx.
     * Здесь создается анонимный класс, который определяет наши часы.
     */
    public AnimationTimer clock() {
        return new AnimationTimer() {
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
    }
}
