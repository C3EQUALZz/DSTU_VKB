package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;
import javafx.scene.control.Button;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readersFromDatabase.readingPhotoFromDatabase.PhotoReader;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;

/**
 * Класс, который является настройкой, чтобы настроить кнопку просмотра фото.
 */
@RequiredArgsConstructor
public class ReaderPlanActionViewDatabase implements ActionViewingDatabase {

    private final TableViewContext context;
    private final Button button;
    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();

    /**
     * Точка запуска логики
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(button, mouseEvent -> new PhotoReader(context.customersTableView(), button).event());
    }
}
