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
import java.util.HashSet;
import java.util.ResourceBundle;

public class MenuAddress extends BaseController {

    @FXML
    private MapView mapView;
    @FXML
    private Button downloadFile, startSearch, addHuman, createDocument, addDataToDB, backButton;
    @FXML
    private TextField addressField, fullNameField;
    @FXML
    private ComboBox<String> combobox;

    private final ComboboxConfigurator comboboxConfigurator = new ComboboxConfigurator();
    private HashSet<String> persons;
    private FileChooserController fileChooserController;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        comboboxConfigurator.defaultConfiguration(combobox);

        initializeMap();
        initializeSearchEngine();
        initializeFullName();
        initializeCreateDocument();
        initializeFileChooser();
        overRideBackButton();

        new FormObserver(addressField, combobox, Arrays.asList(createDocument, addDataToDB));
    }

    /**
     * Здесь запускается event, который обрабатывает изначальную инициализацию карты, добавляет event маркера
     */
    private void initializeMap() {
        var openStreetMapInstance = new OpenStreetMap(mapView);
        openStreetMapInstance.setAddressField(addressField);
        openStreetMapInstance.event();
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
        fileChooserController = new FileChooserController();
        buttonConfigurator.setupButtonEvent(downloadFile, event -> fileChooserController.event(event));
    }

    /**
     * Здесь запускается event, который обрабатывает добавления ФИО в TextField.
     * После добавления хотя бы одного ФИО включается combobox.
     */
    private void initializeFullName() {
        var textFieldAddController = new TextFieldAddController(fullNameField);

        buttonConfigurator.setupButtonEvent(addHuman, event -> {
            persons = textFieldAddController.event();
            comboboxConfigurator.setupComboboxEvent(combobox, persons);
        });
    }

    /**
     * Здесь описывается логика создания документа, который мы будем обрабатывать.
     */
    private void initializeCreateDocument() {
        // Словарь, в котором мы будем хранить все значения
        var jsonData = new HashMap<String, String>();

        var docxProcessor = new DocxProcessor(jsonData);
        buttonConfigurator.setupButtonEvent(createDocument, event -> {
            // Добавляем значения в наш словарь
            jsonData.put("addressField", addressField.getText());
            jsonData.put("fullNameField", fullNameField.getText());
            jsonData.put("mainPerson", combobox.getValue());
            jsonData.put("buildingPlan", fileChooserController.getSelectedFile());
            jsonData.put("allPeople", String.join(", ", persons));
            jsonData.put("pathToFile", docxProcessor.event());
        });
    }

    /**
     * Нужно было переопределить кнопку возвращения назад в меню проекта
     */
    private void overRideBackButton() {
        buttonConfigurator.setupButtonEvent(
                backButton,
                event -> controller.switchFromFillingFormToProjectMenu(),
                "Не получилось переключиться на меню проекта с окна записи данных в БД"
        );
    }

}