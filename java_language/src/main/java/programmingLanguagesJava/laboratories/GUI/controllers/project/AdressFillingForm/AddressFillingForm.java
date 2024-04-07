/**
 * Контроллер для взаимодействия с адресом
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import com.sothawo.mapjfx.MapView;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.fileChooserInteraction.FileChooserController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.observers.FormObserver;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy.*;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategyContext.StrategyContextMap;

import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;
import java.util.ResourceBundle;
import java.util.stream.Stream;

/**
 * Контроллер для окна для ввода данных от оператора
 */
public class AddressFillingForm extends BaseController {

    @FXML
    private MapView mapView;
    @FXML
    private Button downloadFile, startSearch, addHuman, createDocument, addDataToDB;
    @FXML
    private TextField addressField, fullNameField;
    @FXML
    private ComboBox<String> combobox;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        var strategyMap = new StrategyContextMap(mapView, addressField);
        var fileChooser = new FileChooserController();
        var jsonData = new HashMap<String, String>();

        // TODO: добавить многопоточный запуск, настроить все

        Stream.of(
                new TextFieldAddControllerActionFillingForm(fullNameField, addHuman, combobox),
                new TextFieldSearchControllerActionFillingForm(strategyMap, startSearch),
                new OpenStreetMapActionFillingForm(strategyMap),
                new FileChooserActionFillingForm(fileChooser, downloadFile),
                new AddDataToDatabaseActionFillingForm(jsonData, addDataToDB),
                new CreateDocumentActionFillingForm(fileChooser, jsonData, createDocument, addressField, combobox)
        ).forEach(ActionFillingForm::execute);


        new FormObserver(addressField, combobox, Arrays.asList(createDocument, addDataToDB)).listen();
    }
}