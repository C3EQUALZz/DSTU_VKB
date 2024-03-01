/*
 * Данный модуль описывает контроллеры (обработчики событий для Меню)
 * Здесь определены действия для кнопок, часов, плеера (звук при наведении на кнопки)
 */

package programmingLanguagesJava.laboratories.GUI.controllers.menu;



import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.text.Text;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;
public class Menu extends BaseController {

    @FXML private Button ButtonLabs, ButtonProject;
    @FXML private Text secondsTimer, minutesTimer, hourTimer;

    /**
     * Здесь вот точка запуска программы контроллеров происходит. Параметрами я даже не пользуюсь, но они нужны.
     */
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        super.initialize(url, resourceBundle);

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

    }
}
