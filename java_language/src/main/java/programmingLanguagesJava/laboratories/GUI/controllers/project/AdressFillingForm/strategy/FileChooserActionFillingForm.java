package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.fileChooserInteraction.FileChooserController;

public class FileChooserActionFillingForm implements ActionFillingForm {

    private final FileChooserController fileChooserController;
    private final Button downloadFile;

    public FileChooserActionFillingForm(Button downloadFile) {
        this.fileChooserController = new FileChooserController();
        this.downloadFile = downloadFile;
    }

    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(downloadFile, fileChooserController::event);
    }
}
