package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;

import java.net.URL;
import java.util.ResourceBundle;

public class ViewData extends BaseController {

    @FXML private Button backButton;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        setbackButton();
    }

    
    private void setbackButton() {
        buttonConfigurator.setupButtonEvent(
                backButton,
                event -> controller.switchToMenuProject(),
                "Не получилось переключиться на меню проекта ");
    }
}
