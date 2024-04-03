/**
 * Данный класс отвечает за часы, которые есть в главном меню.
 * Гайд, по которому я это делал: https://youtu.be/8zOSqvKNTlY?si=dqK8oV0rOkG9LlOy
 */

package programmingLanguagesJava.laboratories.GUI.controllers.menu;

import javafx.animation.AnimationTimer;
import javafx.application.Platform;
import javafx.scene.text.Text;
import lombok.RequiredArgsConstructor;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@RequiredArgsConstructor
class ClockController implements ElementMenu {
    private final Text hourTimer, minutesTimer, secondsTimer;


    /**
     * Здесь создается анонимный класс, который определяет наши часы.
     * Здесь уже автоматически происходит подстановка значений.
     * Все изменения в UI нужно делать в одном потоке по правилам JavaFx.
     *
     * @return возвращает наш таймер
     */
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
     * Точка запуска контроллера для часов.
     */
    @Override
    public void event() {
        createTimer().start();
    }
}
