package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readersFromDatabase.readingPhotoFromDatabase;

import javafx.scene.control.Button;
import javafx.scene.control.TableView;

import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readersFromDatabase.FileOpener;

/**
 * Класс, чтобы просматривать фотографии, когда нажали на кнопку на окне.
 */
public class PhotoReader extends FileOpener {

    public PhotoReader(TableView<PersonInfo> customersTableView, Button button) {
        super(customersTableView, button);
    }

    /**
     * Точка запуска
     */
    @Override
    public void event() {
        buttonConfigurator.setupButtonEvent(button, mouseEvent -> {
            PersonInfo selectedPerson = customersTableView.getSelectionModel().getSelectedItem();
            openFile(selectedPerson.getPlanOfHouse(), ".png");
        });
    }
}
