package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase;

import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

import java.net.URL;
import java.util.ResourceBundle;


public class ViewData extends BaseController {
    @FXML private TableView<PersonInfo> customersTableView;
    @FXML private TableColumn<PersonInfo, String> surnameColumn, nameColumn, patronymicColumn, planColumn, pactColumn;
    private final DatabaseLoader databaseLoader = new DatabaseLoader();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        loadData();
    }


    private void loadData() {
        surnameColumn.setCellValueFactory(new PropertyValueFactory<>("lastName"));
        nameColumn.setCellValueFactory(new PropertyValueFactory<>("firstName"));
        patronymicColumn.setCellValueFactory(new PropertyValueFactory<>("patronymic"));
        planColumn.setCellValueFactory(new PropertyValueFactory<>("planOfHouse"));
        pactColumn.setCellValueFactory(new PropertyValueFactory<>("document"));

        var personInfos = databaseLoader.loadPersonInfos();
        customersTableView.setItems(FXCollections.observableArrayList(personInfos));
    }

}
