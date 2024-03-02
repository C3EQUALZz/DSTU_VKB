package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import com.sothawo.mapjfx.MapView;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;

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
        new OpenStreetMap(mapView, addressField).mapViewEvent();
        PhotoAutoCadFileChooser.fileChooserEvent(downloadFile, buttonConfigurator);
    }


}
