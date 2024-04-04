package programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy;

import javafx.scene.text.Text;
import programmingLanguagesJava.laboratories.GUI.controllers.menu.ClockController;
import lombok.RequiredArgsConstructor;

/**
 * Данный класс является одним из посредников для удобного запуска элементов UI.
 * Реализован паттерн стратегия.
 * Здесь прослойка для запуска часов.
 */
@RequiredArgsConstructor
public class ClockControllerActionMainMenu implements ActionMainMenu {

    private final Text secondsTimer, minutesTimer, hourTimer;

    /**
     * Точка запуска
     */
    @Override
    public void execute() {
        new ClockController(hourTimer, minutesTimer, secondsTimer).event();
    }
}
