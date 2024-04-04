/**
 * Контроллер, который отвечает за взаимодействие с окном, где расположена таблица с базой данных.
 * Источники, которые я использовал: https://youtu.be/V9nDH2iBJSM?si=aO98-8AkltxZj2sK
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase;

import javafx.collections.FXCollections;
import javafx.collections.transformation.FilteredList;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.DataBaseSQLite;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.HumanSearchController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy.FirstNameSearchStrategy;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy.LastNameSearchStrategy;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy.PatronymicSearchStrategy;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.tableViewStart.TableViewManager;

import java.net.URL;
import java.util.Arrays;
import java.util.List;
import java.util.ResourceBundle;


public class ViewData extends BaseController {
    @FXML private TableView<PersonInfo> customersTableView;
    @FXML private TableColumn<PersonInfo, String> surnameColumn, nameColumn, patronymicColumn;
    @FXML private TableColumn<PersonInfo, Image> planColumn, pactColumn;
    @FXML private Button addHumanButton, updateTableButton;
    @FXML private TextField keywordTextField;
    @FXML private ComboBox<String> sortValueCombobox;

    private final DataBaseSQLite database = DataBaseSQLite.getInstance();
    private final ComboboxConfigurator comboboxConfigurator = ComboboxConfigurator.getInstance();
    private final List<PersonInfo> personInfos = database.loadPersonInfos();


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        comboboxConfigurator.defaultConfiguration(sortValueCombobox);

        setTableView();
        setAddHumanButton();
        setKeywordTextField();
        setUpdateTableButton();

    }

    private void setTableView() {
        TableViewManager.builder().customersTableView(customersTableView).surnameColumn(surnameColumn).nameColumn(nameColumn).
                patronymicColumn(patronymicColumn).planColumn(planColumn).pactColumn(pactColumn).database(database)
                .personInfos(personInfos).build().event();
    }

    private void setAddHumanButton() {
        buttonConfigurator.setupButtonEvent(addHumanButton, event -> controller.switchFromDataBaseViewToFillingForm());
    }

    private void setKeywordTextField() {
         HumanSearchController.builder()
                .customersTableView(customersTableView)
                .filteredData(new FilteredList<>(FXCollections.observableArrayList(personInfos)))
                .keywordTextField(keywordTextField)
                .searchStrategies(Arrays.asList(new FirstNameSearchStrategy(), new LastNameSearchStrategy(), new PatronymicSearchStrategy()))
                .build().event();
    }

    private void setUpdateTableButton() {
        buttonConfigurator.setupButtonEvent(updateTableButton, event -> setTableView());
    }



}
