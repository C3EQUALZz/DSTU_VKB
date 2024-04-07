package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.scene.control.Button;
import lombok.RequiredArgsConstructor;

/**
 * Конфигурация кнопки, чтобы отправлять на форму с добавлением людей.
 */
@RequiredArgsConstructor
public class AddHumanButtonActionViewingDatabase implements ActionViewingDatabase {

    private final Button addHumanButton;

    /**
     * Точка запуска программы.
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(addHumanButton, event -> controller.switchFromDataBaseViewToFillingForm());
    }

}
