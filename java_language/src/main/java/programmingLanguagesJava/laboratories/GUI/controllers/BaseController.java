/**
 * Этот контроллер создан с той целью, чтобы убрать дублирование кода во многих классах.
 * Разные окна имеют некоторый одинаковый функционал, поэтому я вынес в один абстрактный класс
 */

package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.animation.PauseTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.util.Duration;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public abstract class BaseController implements Initializable {
    @FXML
    private Button exitButton, backButton;
    private final ButtonConfigurator buttonConfigurator = new ButtonConfigurator();
    private final SceneController controller = new SceneController();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        // try - catch стоит, так как у нас в главном меню, где стоит выбор лабораторных и приложений
        // нет backButton. Ему важно, чтобы все ID были, поэтому вот такой костыль, чтобы убрать повторы кода.

        try {
            // Обработка событий для кнопки с выходом из приложения

            buttonConfigurator.setupButtonEvent(exitButton, event -> {

                PauseTransition pause = new PauseTransition(Duration.millis(100));
                pause.setOnFinished(evt -> Platform.exit());
                pause.play();

            });

            // Обработка событий возврата обратно в меню
            buttonConfigurator.setupButtonEvent(backButton, event -> {

                try {
                    controller.switchToMenu(event);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }

            });

        } catch (RuntimeException ignored) {}
    }

}
