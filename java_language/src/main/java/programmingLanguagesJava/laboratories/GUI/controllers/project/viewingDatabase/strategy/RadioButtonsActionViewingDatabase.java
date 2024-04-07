package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.collections.ObservableList;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.sortingDatabase.SorterTableView;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.RadioButtonContext;

/**
 * Класс, который конфигурирует radio Button
 */
@RequiredArgsConstructor
public class RadioButtonsActionViewingDatabase implements ActionViewingDatabase {

    private final ObservableList<PersonInfo> personInfos;
    private final RadioButtonContext radioButtonContext;

    /**
     * Точка запуска этого кода.
     */
    @Override
    public void execute() {

        new SorterTableView(
                radioButtonContext.lastNameRadioButton(),
                radioButtonContext.firstNameRadioButton(),
                radioButtonContext.patronymicRadioButton(),
                personInfos).event();
    }
}
