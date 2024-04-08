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
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy.*;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.RadioButtonContext;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;

import java.net.URL;
import java.util.ResourceBundle;
import java.util.stream.Stream;

/**
 * Контроллер для Scene с просмотром базы данных
 */
public class ViewData extends BaseController {
    @FXML
    private TableView<PersonInfo> customersTableView;
    @FXML
    private TableColumn<PersonInfo, String> surnameColumn, nameColumn, patronymicColumn;
    @FXML
    private TableColumn<PersonInfo, Image> planColumn, pactColumn;
    @FXML
    private Button addHumanButton, updateTableButton, planOfhouseButton, contractButton, deleteRowButton;
    @FXML
    private TextField keywordTextField;
    @FXML
    private RadioButton lastNameRadioButton, firstNameRadioButton, patronymicRadioButton;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        var context = new TableViewContext(
                customersTableView,
                surnameColumn,
                nameColumn,
                patronymicColumn,
                planColumn,
                pactColumn
        );

        var radioButtonContext = new RadioButtonContext(
                lastNameRadioButton,
                firstNameRadioButton,
                patronymicRadioButton
        );


        var listDataBase = FXCollections.observableArrayList(DataBaseSQLite.getInstance().loadPersonInfos());

        Stream.of(
                new AddHumanButtonActionViewingDatabase(addHumanButton),
                new TableViewConfActionViewingDatabase(listDataBase, context),
                new KeyWordTextFieldActionViewingDatabase(listDataBase, context, keywordTextField),
                new RadioButtonsActionViewingDatabase(listDataBase, radioButtonContext),
                new UpdateTableButtonActionViewingDatabase(listDataBase, context, radioButtonContext,
                        updateTableButton, keywordTextField),
                new ReaderActionViewingDataBase(context, contractButton),
                new ReaderPlanActionViewDatabase(context, planOfhouseButton),
                new DeleteRowActionViewingDatabase(context, deleteRowButton)

        ).forEach(ActionViewingDatabase::execute);

    }


}
