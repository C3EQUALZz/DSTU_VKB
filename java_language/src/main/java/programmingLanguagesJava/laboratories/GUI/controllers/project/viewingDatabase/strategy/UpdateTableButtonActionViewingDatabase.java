package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import lombok.AllArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.DataBaseSQLite;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.RadioButtonContext;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;

/**
 * Класс, который конфигурирует кнопку обновления таблицы.
 */
@AllArgsConstructor
public class UpdateTableButtonActionViewingDatabase implements ActionViewingDatabase {

    private ObservableList<PersonInfo> list;
    private final TableViewContext context;
    private final RadioButtonContext radioButtonContext;

    private final Button updateTableButton;
    private final TextField textField;

    /**
     * Точка запуска
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(updateTableButton, event -> {
            list = FXCollections.observableArrayList(DataBaseSQLite.getInstance().loadPersonInfos());

            new TableViewConfActionViewingDatabase(list, context).execute();
            new KeyWordTextFieldActionViewingDatabase(list, context, textField).execute();
            new RadioButtonsActionViewingDatabase(list, radioButtonContext).execute();
            context.customersTableView().refresh();
        });
    }
}
