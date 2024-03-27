/**
 * Контроллер для взаимодействия с адресом
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import com.sothawo.mapjfx.MapView;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.addingNames.TextFieldAddController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing.DocxProcessor;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.fileChooserInteraction.FileChooserController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.observers.FormObserver;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.processingEventsOnMap.OpenStreetMap;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.searchEngineField.TextFieldSearchController;

import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;
import java.util.ResourceBundle;

public class MenuAddress extends BaseController {

    @FXML private MapView mapView;
    @FXML private Button downloadFile, startSearch, addHuman, createDocument, addDataToDB;
    @FXML private TextField addressField, fullNameField;
    @FXML private ComboBox<String> combobox;

    private final ComboboxConfigurator comboboxConfigurator = new ComboboxConfigurator();
    private final HashMap<String, String> jsonData = new HashMap<>();


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        comboboxConfigurator.defaultConfiguration(combobox);

        initializeMap();
        initializeSearchEngine();
        initializeFullName();
        initializeCreateDocument();
        initializeFileChooser();

        new FormObserver(addressField, combobox, Arrays.asList(createDocument, addDataToDB));
    }

    /**
     * Здесь запускается event, который обрабатывает изначальную инициализацию карты, добавляет event маркера
     */
    private void initializeMap() {
        var openStreetMapInstance = new OpenStreetMap(mapView);
        openStreetMapInstance.setAddressField(addressField);
        openStreetMapInstance.event();

        addressField.textProperty().addListener((observable, oldValue, newValue) -> updateJsonData("addressField", newValue));
    }

    /**
     * Здесь запускается event, который обрабатывает поиск через ввод данных с TextField.
     */
    private void initializeSearchEngine() {
        var textFieldSearchController = new TextFieldSearchController(addressField);
        textFieldSearchController.setMapView(mapView);
        buttonConfigurator.setupButtonEvent(startSearch, event -> textFieldSearchController.event());
    }

    /**
     * Здесь запускается event, который обрабатывает кнопку добавки файлов
     */
    private void initializeFileChooser() {
        var fileChooserController = new FileChooserController();
        buttonConfigurator.setupButtonEvent(downloadFile, event -> updateJsonData("buildingPlan", fileChooserController.event(event)));
    }

    /**
     * Здесь запускается event, который обрабатывает добавления ФИО в TextField.
     * После добавления хотя бы одного ФИО включается combobox.
     */
    private void initializeFullName() {
        var textFieldAddController = new TextFieldAddController(fullNameField);

        buttonConfigurator.setupButtonEvent(addHuman, event -> {
            var persons = textFieldAddController.event();
            comboboxConfigurator.setupComboboxEvent(combobox, persons);
            updateJsonData("allPeople", String.join(", ", persons));
            combobox.getSelectionModel().selectedItemProperty().addListener((observable, oldValue, newValue) -> updateJsonData("mainPerson", newValue));
        });
    }

    /**
     * Здесь описывается логика создания документа, который мы будем обрабатывать.
     */
    private void initializeCreateDocument() {
        var docxProcessor = new DocxProcessor(this.jsonData);
        buttonConfigurator.setupButtonEvent(createDocument, event -> updateJsonData("pathToFile", docxProcessor.event()));
    }

    private void updateJsonData(String elementUI, String value) {
        jsonData.put(elementUI, value);
    }
}