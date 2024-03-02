package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import com.sothawo.mapjfx.MapView;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import javafx.stage.FileChooser;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;

import java.io.File;
import java.net.URL;
import java.util.ResourceBundle;

public class MenuAddress extends BaseController {

    @FXML private MapView mapView;
    @FXML private Button downloadFile, startSearch;
    @FXML private TextField addressField;
    @FXML private ComboBox<String> combobox;

    // Операторы выбирают файлы с нужными расширениями, чтобы сохранять информацию об объектах.
    // Например, могут выбрать фото, или файлы для AutoCad, Revit и т.п.
    private final FileChooser.ExtensionFilter
            photosFilter = new FileChooser.ExtensionFilter("Photo", "*.jpg", "*.jpeg", "*.png"),
            autoCadFilesFilter = new FileChooser.ExtensionFilter("Plans", "*.dwg", "*.rvt");

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        new OpenStreetMap(mapView, addressField).mapViewEvent();
        fileChooserEvent();
    }


    private void fileChooserEvent() {
        buttonConfigurator.setupButtonEvent(downloadFile, event -> {

            var fileChooser = new FileChooser();
            fileChooser.setTitle("Выберите файл с планом здания ");
            fileChooser.getExtensionFilters().addAll(photosFilter, autoCadFilesFilter);

            String downloadPath = System.getProperty("user.home") + File.separator + "Downloads";
            fileChooser.setInitialDirectory(new File(downloadPath));

            var selectedFile = fileChooser.showOpenDialog(((Node) event.getSource()).getScene().getWindow());
        });
    }


}
