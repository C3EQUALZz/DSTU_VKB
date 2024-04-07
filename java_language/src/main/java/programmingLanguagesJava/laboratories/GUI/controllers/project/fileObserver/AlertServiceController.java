package programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.stage.Stage;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;

import java.net.URL;
import java.util.ResourceBundle;

public class AlertServiceController implements Initializable {
    @FXML
    private Button closeButton;

    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        buttonConfigurator.setupButtonEvent(closeButton, mouseEvent -> {
            var stage = (Stage) closeButton.getScene().getWindow();
            stage.close();
        });


    }
}
