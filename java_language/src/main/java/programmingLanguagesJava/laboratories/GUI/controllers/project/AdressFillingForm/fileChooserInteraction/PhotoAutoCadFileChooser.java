/**
 * Данная часть разработана как обработчик событий на выбор файлов, который Java сама вызывает относительно операционной системы.
 * Здесь скорее всего будет обработка по добавлению плана здания.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.fileChooserInteraction;

import javafx.scene.Node;
import javafx.scene.input.MouseEvent;
import javafx.stage.FileChooser;

import java.io.File;

public class PhotoAutoCadFileChooser {
    private static final FileChooser.ExtensionFilter photosFilter = new FileChooser.ExtensionFilter("Photo", "*.jpg", "*.jpeg", "*.png");
    private static final FileChooser.ExtensionFilter autoCadFilesFilter = new FileChooser.ExtensionFilter("Plans", "*.dwg", "*.rvt");
    private final FileChooser fileChooser = new FileChooser();

    private String selectedFile;

    @SuppressWarnings("unused")
    public String getSelectedFile() {
        return this.selectedFile;
    }

    @SuppressWarnings("unused")
    public void event(MouseEvent event) {
        fileChooser.setTitle("Выберите файл с планом здания ");
        fileChooser.getExtensionFilters().addAll(photosFilter, autoCadFilesFilter);

        String downloadPath = System.getProperty("user.home") + File.separator + "Downloads";
        fileChooser.setInitialDirectory(new File(downloadPath));

        selectedFile = fileChooser.showOpenDialog(((Node) event.getSource()).getScene().getWindow()).getPath();
    }
}
