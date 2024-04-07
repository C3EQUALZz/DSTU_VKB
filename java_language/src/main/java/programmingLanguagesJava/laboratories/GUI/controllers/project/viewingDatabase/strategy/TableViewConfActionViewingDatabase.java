package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.collections.ObservableList;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.tableViewStart.TableViewManager;
import lombok.RequiredArgsConstructor;

/**
 * Класс, который конфигурирует создание TableView для отображения базы данных в приложении
 */
@RequiredArgsConstructor
public class TableViewConfActionViewingDatabase implements ActionViewingDatabase {
    private final ObservableList<PersonInfo> personInfos;
    private final TableViewContext context;

    /**
     * Точка запуска
     */
    @Override
    public void execute() {

        new TableViewManager(
                context.customersTableView(),
                context.surnameColumn(),
                context.nameColumn(),
                context.patronymicColumn(),
                context.planColumn(),
                context.pactColumn(),
                personInfos
        ).event();
    }
}
