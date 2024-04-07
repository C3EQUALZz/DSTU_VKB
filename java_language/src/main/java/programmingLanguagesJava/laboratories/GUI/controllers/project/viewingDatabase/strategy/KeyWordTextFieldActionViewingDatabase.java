package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.collections.ObservableList;
import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.HumanSearchController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class KeyWordTextFieldActionViewingDatabase implements ActionViewingDatabase {

    private final ObservableList<PersonInfo> personInfos;
    private final TableViewContext context;
    private final TextField keywordTextField;

    @Override
    public void execute() {
        HumanSearchController.builder()
                .customersTableView(context.customersTableView())
                .keywordTextField(keywordTextField)
                .personInfos(personInfos)
                .build().event();
    }
}
