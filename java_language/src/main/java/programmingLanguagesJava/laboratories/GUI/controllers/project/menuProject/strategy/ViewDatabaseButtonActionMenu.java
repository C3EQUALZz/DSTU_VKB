package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;
import lombok.RequiredArgsConstructor;

/**
 * Данный класс является одним из посредников для удобного запуска элементов UI.
 * Реализован паттерн стратегия.
 * Здесь происходит настройка переключения с меню на просмотр базы данных
 */
@RequiredArgsConstructor
public class ViewDatabaseButtonActionMenu implements ActionMenu {

    private final Button viewDatabaseButton;
    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    private final SceneController controller = SceneController.getInstance();

    /**
     * Точка запуска
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(
                viewDatabaseButton,
                event -> controller.switchFromMenuProjectToDataBaseView(),
                "Не получилось переключиться на страницу с просмотром БД"
        );
    }
}
