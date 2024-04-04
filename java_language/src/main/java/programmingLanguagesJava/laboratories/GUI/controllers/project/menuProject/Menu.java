/**
 * Здесь описывается меню проекта
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.scene.media.MediaView;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.movableAnchor.MovableAnchorPane;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.observers.TextFieldsObserver;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.webViewVideo.VideoPlayer;

import java.net.URL;
import java.util.ResourceBundle;

public class Menu extends BaseController {

    @FXML private AnchorPane anchorPaneMovable, registrationAnchorPane;
    @FXML private Button signInButton, addToDatabaseButton, viewDatabaseButton;
    @FXML private MediaView mediaViewVideo;
    @FXML private TextField loginField;
    @FXML private PasswordField passwordField;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        setWebViewVideo();
        setSignInButton();
        setAddToDatabaseButton();
        setViewDatabaseButton();

        new TextFieldsObserver(loginField, passwordField, signInButton).listen();

    }

    /**
     * Настройка подключения, когда пользователь входит в приложение
     */
    private void setSignInButton() {
        var movableAnchorPane = new MovableAnchorPane(anchorPaneMovable, registrationAnchorPane);
        buttonConfigurator.setupButtonEvent(signInButton, event -> movableAnchorPane.event());
    }

    /**
     * Настройка видео
     */
    private void setWebViewVideo() {
        var videoPlayer = new VideoPlayer(mediaViewVideo);
        videoPlayer.event();
    }

    /**
     * Настройка переключения на форму с базой данных
     */
    private void setAddToDatabaseButton() {
        buttonConfigurator.setupButtonEvent(
                addToDatabaseButton,
                event -> controller.switchFromMenuProjectToFillingForm(),
                "Не получилось переключиться на страницу с заполнением БД"
        );

    }

    /**
     * Настройка переключения с меню на просмотр базы данных
     */
    private void setViewDatabaseButton() {
        buttonConfigurator.setupButtonEvent(
                viewDatabaseButton,
                event -> controller.switchFromMenuProjectToDataBaseView(),
                "Не получилось переключиться на страницу с просмотром БД"
            );
    }

}
