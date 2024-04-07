/**
 * Контроллер, который отвечает за взаимодействие с окном, где расположена таблица с базой данных.
 * Источники, которые я использовал: https://youtu.be/V9nDH2iBJSM?si=aO98-8AkltxZj2sK
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase;

import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.DataBaseSQLite;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.HumanSearchController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy.FirstNameSearchStrategy;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy.LastNameSearchStrategy;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy.PatronymicSearchStrategy;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.sortingDatabase.SorterTableView;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.tableViewStart.TableViewManager;

import java.net.URL;
import java.util.Arrays;
import java.util.ResourceBundle;


public class ViewData extends BaseController {
    @FXML
    private TableView<PersonInfo> customersTableView;
    @FXML
    private TableColumn<PersonInfo, String> surnameColumn, nameColumn, patronymicColumn;
    @FXML
    private TableColumn<PersonInfo, Image> planColumn, pactColumn;
    @FXML
    private Button addHumanButton, updateTableButton;
    @FXML
    private TextField keywordTextField;
    @FXML
    private RadioButton lastNameRadioButton, firstNameRadioButton, patronymicRadioButton;


    private final DataBaseSQLite database = DataBaseSQLite.getInstance();


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        setTableView();
        setAddHumanButton();
        setKeywordTextField();
        setUpdateTableButton();
        setLastNameRadioButton();

    }

    private void setTableView() {
        TableViewManager.builder().customersTableView(customersTableView).surnameColumn(surnameColumn).nameColumn(nameColumn).
                patronymicColumn(patronymicColumn).planColumn(planColumn).pactColumn(pactColumn).database(database)
                .personInfos(database.loadPersonInfos()).build().event();
    }

    private void setAddHumanButton() {
        buttonConfigurator.setupButtonEvent(addHumanButton, event -> controller.switchFromDataBaseViewToFillingForm());
    }

    private void setKeywordTextField() {
        HumanSearchController.builder()
                .customersTableView(customersTableView)
                .personInfos(FXCollections.observableArrayList(database.loadPersonInfos()))
                .keywordTextField(keywordTextField)
                .searchStrategies(Arrays.asList(new FirstNameSearchStrategy(), new LastNameSearchStrategy(), new PatronymicSearchStrategy()))
                .build().event();
    }

    private void setUpdateTableButton() {
        buttonConfigurator.setupButtonEvent(updateTableButton, event -> {
            setTableView();
            customersTableView.refresh();
        });
    }

    private void setLastNameRadioButton() {
        // Создание ObservableList с данными
        var data = FXCollections.observableArrayList(database.loadPersonInfos());

        // Установка ObservableList в качестве элементов TableView
        customersTableView.setItems(data);

        SorterTableView.builder().data(data)
                .firstNameRadioButton(firstNameRadioButton)
                .lastNameRadioButton(lastNameRadioButton)
                .patronymicRadioButton(patronymicRadioButton).build().event();

    }


}
