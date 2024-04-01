/**
 * Данная часть разработана как обработчик событий на выбор файлов, который Java сама вызывает относительно операционной системы.
 * Здесь скорее всего будет обработка по добавлению плана здания.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.fileChooserInteraction;

import javafx.scene.Node;
import javafx.scene.input.MouseEvent;
import javafx.stage.FileChooser;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.ElementAddressFillingForm;

import java.io.File;
import java.util.List;

public class FileChooserController implements ElementAddressFillingForm {

    // Фильтры для файлов, которые нам нужны. Я изначально планирую только фото или файлы AutoCad/Revit
    List<FileChooser.ExtensionFilter> filters = List.of(
            new FileChooser.ExtensionFilter("Photo", "*.jpg", "*.jpeg", "*.png"),
            new FileChooser.ExtensionFilter("Plans", "*.dwg", "*.rvt")
    );
    private File selectedFile;

    private final FileChooser fileChooser;

    /**
     * Контроллер, который отвечает за выбор файлов путем вызова окна ОС
     */
    public FileChooserController() {
        this.fileChooser = new FileChooser();
        this.fileChooser.setTitle("Выберите файл с планом здания");
        this.fileChooser.getExtensionFilters().addAll(filters);
        this.fileChooser.setInitialDirectory(new File(System.getProperty("user.home") + File.separator + "Downloads"));
    }

    /**
     * Обработчик событий выбора файла посредством OC.
     * @param event данный event нужен, чтобы можно было вызвать окно выбора файла, ссылаясь на stage.
     */
    public void event(MouseEvent event) {
        selectedFile = this.fileChooser.showOpenDialog(((Node) event.getSource()).getScene().getWindow());
    }

    /**
     *  @return возвращает путь к выбранному файлу, если пользователь выбрал
     */
    public String getSelectedFile() {
        return selectedFile != null ? selectedFile.getPath() : null;
    }
}
