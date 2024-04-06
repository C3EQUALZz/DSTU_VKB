package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.fileChooserInteraction.FileChooserController;
import lombok.RequiredArgsConstructor;

/**
 * Здесь класс, который является опять-таки прослойкой для конфигурации FileChooserController
 */
@RequiredArgsConstructor
public class FileChooserActionFillingForm implements ActionFillingForm {

    private final FileChooserController fileChooserController;
    private final Button downloadFile;

    /**
     * Точка запуска программы
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(downloadFile, fileChooserController::event);
    }
}
