/**
 * Данный класс отвечает за часы, которые есть в главном меню
 */

package programmingLanguagesJava.laboratories.GUI.controllers.menu;

import javafx.animation.AnimationTimer;
import javafx.application.Platform;
import javafx.scene.text.Text;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

class ClockController implements ElementMenu {
    private final Text hourTimer, minutesTimer, secondsTimer;

    ClockController(Text hourTimer, Text minutesTimer, Text secondsTimer) {
        this.hourTimer = hourTimer;
        this.minutesTimer = minutesTimer;
        this.secondsTimer = secondsTimer;
    }

    private AnimationTimer createTimer() {
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

    /**
     * Контроллер для часов.
     * Все изменения в UI нужно делать в одном потоке по правилам JavaFx.
     * Здесь создается анонимный класс, который определяет наши часы.
     */
    @Override
    public void event() {
        createTimer().start();
    }
}
