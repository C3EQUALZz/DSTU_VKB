package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.strategy;

import javafx.scene.control.Button;
import javafx.scene.layout.AnchorPane;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.movableAnchor.MovableAnchorPane;
import lombok.RequiredArgsConstructor;

/**
 * Данный класс является одним из посредников для удобного запуска элементов UI.
 * Реализован паттерн стратегия.
 * Здесь происходит настройка подключения, когда пользователь входит в приложение
 */

@RequiredArgsConstructor
public class SignInButtonActionMenu implements ActionMenu {

    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    private final AnchorPane anchorPaneMovable, registrationAnchorPane;
    private final Button signInButton;

    /**
     * Точка запуска
     */
    @Override
    public void execute() {
        var movableAnchorPane = new MovableAnchorPane(anchorPaneMovable, registrationAnchorPane);
        buttonConfigurator.setupButtonEvent(signInButton, event -> movableAnchorPane.event());
    }
}
