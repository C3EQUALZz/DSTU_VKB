package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.layout.AnchorPane;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.movableAnchor.MovableAnchorPane;

import java.net.URL;
import java.util.ResourceBundle;

public class Menu extends BaseController {

    @FXML private AnchorPane anchorPaneMovable, registrationAnchorPane;
    @FXML private Button signInButton;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        setSignInButton();
    }

    private void setSignInButton() {
        var movableAnchorPane = new MovableAnchorPane(anchorPaneMovable, registrationAnchorPane);
        buttonConfigurator.setupButtonEvent(signInButton, event -> movableAnchorPane.event());
    }

}
