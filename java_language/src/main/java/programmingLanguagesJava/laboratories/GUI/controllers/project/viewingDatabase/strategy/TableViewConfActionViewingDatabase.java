package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.collections.ObservableList;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.tableViewStart.TableViewManager;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class TableViewConfActionViewingDatabase implements ActionViewingDatabase {
    private final ObservableList<PersonInfo> personInfos;
    private final TableViewContext context;

    @Override
    public void execute() {
        TableViewManager.builder().
                customersTableView(context.customersTableView())
                .surnameColumn(context.surnameColumn())
                .nameColumn(context.nameColumn())
                .patronymicColumn(context.patronymicColumn())
                .planColumn(context.planColumn())
                .pactColumn(context.pactColumn())
                .personInfos(personInfos)
                .build().event();
    }
}
