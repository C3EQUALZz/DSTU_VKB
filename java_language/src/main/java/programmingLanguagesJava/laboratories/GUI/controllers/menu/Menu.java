/*
 * Данный модуль описывает контроллеры (обработчики событий для Меню)
 * Здесь определены действия для кнопок, часов, плеера (звук при наведении на кнопки)
 */

package programmingLanguagesJava.laboratories.GUI.controllers.menu;


import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.text.Text;
import programmingLanguagesJava.laboratories.GUI.controllers.BaseController;
import programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy.ActionMainMenu;
import programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy.ButtonLabsActionMainMenu;
import programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy.ButtonProjectActionMainMenu;
import programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy.ClockControllerActionMainMenu;

import java.net.URL;
import java.util.ResourceBundle;
import java.util.stream.Stream;

public class Menu extends BaseController {

    @FXML private Button ButtonLabs, ButtonProject;
    @FXML private Text secondsTimer, minutesTimer, hourTimer;

    /**
     * Здесь вот точка запуска программы контроллеров происходит. Параметрами я даже не пользуюсь, но они нужны.
     */
    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        super.initialize(url, resourceBundle);

        Stream.of(
                new ButtonLabsActionMainMenu(ButtonLabs),
                new ButtonProjectActionMainMenu(ButtonProject),
                new ClockControllerActionMainMenu(secondsTimer, minutesTimer, hourTimer)
        ).parallel().forEach(ActionMainMenu::execute);
    }
}