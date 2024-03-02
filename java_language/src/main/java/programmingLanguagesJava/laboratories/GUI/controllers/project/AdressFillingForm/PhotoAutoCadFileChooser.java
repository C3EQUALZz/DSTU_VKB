package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.stage.FileChooser;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;

import java.io.File;

class PhotoAutoCadFileChooser {
    private static final FileChooser.ExtensionFilter
            photosFilter = new FileChooser.ExtensionFilter("Photo", "*.jpg", "*.jpeg", "*.png");
    private static final FileChooser.ExtensionFilter autoCadFilesFilter = new FileChooser.ExtensionFilter("Plans", "*.dwg", "*.rvt");

    static void fileChooserEvent(Button downloadFile, ButtonConfigurator buttonConfigurator) {
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
