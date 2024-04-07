package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext;

import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.image.Image;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

public record TableViewContext(
        TableView<PersonInfo> customersTableView,
        TableColumn<PersonInfo, String> surnameColumn,
        TableColumn<PersonInfo, String> nameColumn,
        TableColumn<PersonInfo, String> patronymicColumn,
        TableColumn<PersonInfo, Image> planColumn,
        TableColumn<PersonInfo, Image> pactColumn
) {}
