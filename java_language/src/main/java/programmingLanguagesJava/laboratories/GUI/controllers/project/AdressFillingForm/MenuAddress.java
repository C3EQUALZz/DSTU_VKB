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
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.processingEventsOnMap.OpenStreetMap;

import java.net.URL;
import java.util.ResourceBundle;

public class MenuAddress extends BaseController {

    @FXML private MapView mapView;
    @FXML private Button downloadFile, startSearch;
    @FXML private TextField addressField;
    @FXML private ComboBox<String> combobox;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        setUpMap();
        setUpFileChooser();
        setUpSearchEngine();
    }

    /**
     * Здесь запускается event, который обрабатывает изначальную инициализацию карты, добавляет event маркера
     */
    private void setUpMap() {
        var openStreetMapInstance = new OpenStreetMap(mapView);
        openStreetMapInstance.setAddressField(addressField);
        openStreetMapInstance.event();
    }

    /**
     * Здесь запускается event, который обрабатывает поиск через ввод данных с TextField.
     */
    private void setUpSearchEngine() {
        var textFieldSearchEngine = new TextFieldSearchController(addressField);
        textFieldSearchEngine.setMapView(mapView);
        buttonConfigurator.setupButtonEvent(startSearch, event -> textFieldSearchEngine.event());
    }


    /**
     * Здесь запускается event, который обрабатывает кнопку добавки файлов
     */
    private void setUpFileChooser() {
        var fileChooser = new PhotoAutoCadFileChooser();
        fileChooser.setButtonDownloadFile(downloadFile);
        fileChooser.event();

        // Здесь можно добавить логику добавки информации в общий JSON, который позже можно обрабатывать.
    }





}
