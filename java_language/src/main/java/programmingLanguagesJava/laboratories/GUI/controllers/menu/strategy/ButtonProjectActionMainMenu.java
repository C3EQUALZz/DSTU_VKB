package programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy;

import javafx.scene.control.Button;
import lombok.RequiredArgsConstructor;

/**
 * Данный класс является одним из посредников для удобного запуска элементов UI.
 * Реализован паттерн стратегия.
 * Здесь прослойка для открытия проекта.
 */
@RequiredArgsConstructor
public class ButtonProjectActionMainMenu implements ActionMainMenu {

    private final Button ButtonProject;

    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(
                ButtonProject,
                event -> controller.switchToMenuProject(),
                "Не получилось переключиться с меню на проект"
        );
    }
}
