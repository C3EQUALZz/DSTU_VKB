package programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy;

import javafx.scene.control.Button;
import lombok.RequiredArgsConstructor;

/**
 * Данный класс является одним из посредников для удобного запуска элементов UI.
 * Реализован паттерн стратегия.
 * Здесь слой, который отвечает за обработку событий для кнопки с лабораторными
 */
@RequiredArgsConstructor
public class ButtonLabsActionMainMenu implements ActionMainMenu {

    private final Button ButtonLabs;

    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(
                ButtonLabs,
                event -> controller.switchFromMenuToLaboratories(),
                "Не получилось переключиться с меню на лабораторные работы"
        );
    }
}
