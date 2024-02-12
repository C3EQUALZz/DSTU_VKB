/*
 * Данный модуль описывает контроллеры (обработчики событий для Меню)
 * Здесь определены действия для кнопок, часов, плеера (звук при наведении на кнопки)
 */

package programmingLanguagesJava.laboratories.GUI.controllers;


import javafx.animation.PauseTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.text.Text;
import javafx.util.Duration;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public class Menu implements Initializable {

    @FXML
    private Button exitButton;

    @FXML
    private Button ButtonLabs;

    @FXML
    private Button ButtonProject;

    @FXML
    private Text minutesTimer;

    @FXML
    private Text secondsTimer;

    @FXML
    private Text hourTimer;

    private final SceneController controller = new SceneController();
    private final ButtonConfigurator buttonConfigurator = new ButtonConfigurator();

    /**
     * Здесь вот точка запуска программы контроллеров происходит. Параметрами я даже не пользуюсь, но они нужны.
     */
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        // Класс, который описывает часы.

        new ClockController(hourTimer, minutesTimer, secondsTimer).clock().start();

        // Обработка событий для кнопки с лабораторными

        buttonConfigurator.setupButtonEvent(ButtonLabs, event -> {

            try {
                controller.switchFromMenuToLaboratories(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

        // Обработка событий для кнопки с проектом

        buttonConfigurator.setupButtonEvent(ButtonProject, event -> {

            try {
                controller.switchFromMenuToProject(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

        // Обработка событий для кнопки с выходом из меню

        buttonConfigurator.setupButtonEvent(exitButton, event -> {

            PauseTransition pause = new PauseTransition(Duration.millis(100));
            pause.setOnFinished(evt -> Platform.exit());
            pause.play();

        });

    }
}
