package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.deleteRowFromTableView;

import javafx.collections.transformation.FilteredList;
import javafx.scene.control.Button;
import javafx.scene.control.TableView;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;

/**
 * Класс, который отвечает за удаление строк из TableView.
 * Времени нет, чтобы делать удаление из БД, поэтому такое вот сделал.
 */
@RequiredArgsConstructor
public class Deleter implements ElementDatabaseView {

    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    private final TableView<PersonInfo> customersTableView;
    private final Button button;

    /**
     * Точка запуска.
     */
    @Override
    public void event() {
        buttonConfigurator.setupButtonEvent(button, event -> {
            var selectedItem = customersTableView.getSelectionModel().getSelectedItem();
            FilteredList<PersonInfo> filteredData = new FilteredList<>(customersTableView.getItems(), p -> !p.equals(selectedItem));
            customersTableView.setItems(filteredData);
        });
    }
}
