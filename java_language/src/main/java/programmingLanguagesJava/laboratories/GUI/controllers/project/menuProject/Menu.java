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
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.observers.TextFieldsObserver;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.strategy.*;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.strategyContext.ContextAnchorPane;

import java.net.URL;
import java.util.ResourceBundle;
import java.util.stream.Stream;

public class Menu extends BaseController {

    @FXML
    private AnchorPane anchorPaneMovable, registrationAnchorPane, hiddenAnchorPane;
    @FXML
    private Button signInButton, addToDatabaseButton, viewDatabaseButton;
    @FXML
    private MediaView mediaViewVideo;
    @FXML
    private TextField loginField;
    @FXML
    private PasswordField passwordField;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        var context = new ContextAnchorPane(anchorPaneMovable, registrationAnchorPane, hiddenAnchorPane);

        Stream.of(
                new VideoPlayerActionMenu(mediaViewVideo),
                new SignInButtonActionMenu(context, signInButton),
                new AddToDatabaseButtonActionMenu(addToDatabaseButton),
                new ViewDatabaseButtonActionMenu(viewDatabaseButton)
        ).parallel().forEach(ActionMenu::execute);

        new TextFieldsObserver(loginField, passwordField, signInButton).listen();
    }

}
