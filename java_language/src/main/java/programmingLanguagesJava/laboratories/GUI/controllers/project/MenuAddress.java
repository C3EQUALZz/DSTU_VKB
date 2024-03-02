package programmingLanguagesJava.laboratories.GUI.controllers.project;

import com.sothawo.mapjfx.Coordinate;
import com.sothawo.mapjfx.MapView;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.stage.FileChooser;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;

import java.io.File;
import java.net.URL;
import java.util.ResourceBundle;

public class MenuAddress extends BaseController {

    @FXML
    private MapView mapView;

    @FXML
    private Button downloadFile;

    @FXML
    private ComboBox<String> combobox;

    private final FileChooser.ExtensionFilter photosFilter = new FileChooser.ExtensionFilter("Photo",
            "*.jpg", "*.jpeg", "*.png");

    private final FileChooser.ExtensionFilter autoCadFilesFilter = new FileChooser.ExtensionFilter("Plans",
            "*.dwg", "*.rvt");


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);
        mapViewEvent();
        fileChooserEvent();
    }

    private void mapViewEvent() {
        mapView.initialize();
        // Установка начальных координат и масштаба
        mapView.setCenter(new Coordinate(47.2371576587879, 39.711658338598745));
        mapView.setZoom(17);
    }


    private void fileChooserEvent() {
        buttonConfigurator.setupButtonEvent(downloadFile, event -> {

            var fileChooser = new FileChooser();
            fileChooser.setTitle("Выберите файл с планом здания ");
            fileChooser.getExtensionFilters().addAll(photosFilter, autoCadFilesFilter);

            String downloadsPath = System.getProperty("user.home") + File.separator + "Downloads";
            fileChooser.setInitialDirectory(new File(downloadsPath));

            var selectedFile = fileChooser.showOpenDialog(((Node) event.getSource()).getScene().getWindow());
        });
    }


}
