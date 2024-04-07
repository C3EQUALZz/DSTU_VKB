package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readersFromDatabase.readingDocxFromDatabase;

import javafx.scene.control.Button;
import javafx.scene.control.TableView;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readersFromDatabase.FileOpener;

/**
 * Класс, который описывает считыватель файла из БД.
 * Он позволяет просматривать информацию насчет docx документов.
 */
public class Reader extends FileOpener {

    public Reader(TableView<PersonInfo> customersTableView, Button button) {
        super(customersTableView, button);
    }

    /**
     * Точка запуска
     */
    @Override
    public void event() {
        buttonConfigurator.setupButtonEvent(button, mouseEvent -> {
            PersonInfo selectedPerson = customersTableView.getSelectionModel().getSelectedItem();
            openFile(selectedPerson.getDocument(), ".docx");
        });
    }
}
