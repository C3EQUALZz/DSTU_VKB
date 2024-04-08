package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.deleteRowFromTableView.Deleter;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;
import lombok.RequiredArgsConstructor;

/**
 * Настройка для удаления выбранного элемента из TableView
 */
@RequiredArgsConstructor
public class DeleteRowActionViewingDatabase implements ActionViewingDatabase {

    private final TableViewContext context;
    private final Button button;

    /**
     * Точка запуска
     */
    @Override
    public void execute() {
        new Deleter(context.customersTableView(), button).event();
    }
}
