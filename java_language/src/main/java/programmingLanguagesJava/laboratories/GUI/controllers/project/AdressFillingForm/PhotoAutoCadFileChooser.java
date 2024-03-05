package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.stage.FileChooser;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;

import java.io.File;

class PhotoAutoCadFileChooser {
    private static final FileChooser.ExtensionFilter photosFilter = new FileChooser.ExtensionFilter("Photo", "*.jpg", "*.jpeg", "*.png");
    private static final FileChooser.ExtensionFilter autoCadFilesFilter = new FileChooser.ExtensionFilter("Plans", "*.dwg", "*.rvt");
    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();

    private Button buttonDownloadFile;
    private String selectedFile;

    @SuppressWarnings("unused")
    void setButtonDownloadFile(Button button) {
        this.buttonDownloadFile = button;
    }
    @SuppressWarnings("unused")
    Button getButtonDownloadFile() {
        return buttonDownloadFile;
    }

    @SuppressWarnings("unused")
    String getSelectedFile() {
        return this.selectedFile;
    }

    @SuppressWarnings("unused")
    void event() {
        if (buttonDownloadFile == null) {
            throw new RuntimeException("Вы должны выбрать кнопку для установки fileChooser");
        }

        buttonConfigurator.setupButtonEvent(buttonDownloadFile, event -> {

            var fileChooser = new FileChooser();
            fileChooser.setTitle("Выберите файл с планом здания ");
            fileChooser.getExtensionFilters().addAll(photosFilter, autoCadFilesFilter);

            String downloadPath = System.getProperty("user.home") + File.separator + "Downloads";
            fileChooser.setInitialDirectory(new File(downloadPath));

            selectedFile = fileChooser.showOpenDialog(((Node) event.getSource()).getScene().getWindow()).getPath();
        });
    }
}
