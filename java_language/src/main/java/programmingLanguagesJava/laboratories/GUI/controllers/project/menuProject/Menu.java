package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.layout.AnchorPane;
import javafx.scene.media.MediaView;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.movableAnchor.MovableAnchorPane;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.webViewVideo.VideoPlayer;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public class Menu extends BaseController {

    @FXML
    private AnchorPane anchorPaneMovable, registrationAnchorPane;
    @FXML
    private Button signInButton, addToDatabaseButton, viewDatabaseButton;
    @FXML
    private MediaView mediaViewVideo;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        setSignInButton();
        setAddToDatabaseButton();
        setViewDatabaseButton();
        setWebViewVideo();
    }

    private void setSignInButton() {
        var movableAnchorPane = new MovableAnchorPane(anchorPaneMovable, registrationAnchorPane);
        buttonConfigurator.setupButtonEvent(signInButton, event -> movableAnchorPane.event());
    }

    private void setWebViewVideo() {
        var videoPlayer = new VideoPlayer(mediaViewVideo);
        videoPlayer.event();
    }

    private void setAddToDatabaseButton() {
        buttonConfigurator.setupButtonEvent(addToDatabaseButton, event -> {
            try {
                controller.switchFromMenuProjectToFillingForm();
            } catch (IOException e) {
                throw new RuntimeException("Не получилось переключиться на страницу с заполнением БД", e);
            }
        });
    }

    private void setViewDatabaseButton() {
        buttonConfigurator.setupButtonEvent(viewDatabaseButton, event -> {
            try {
                controller.switchFromMenuProjectToDataBaseView();
            } catch (IOException e) {
                throw new RuntimeException("Не получилось переключиться на страницу с просмотром БД", e);
            }
        });
    }

}
