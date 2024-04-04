package programmingLanguagesJava.laboratories.GUI.controllers.menu.strategy;

import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;

public interface ActionMainMenu {

    ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    SceneController controller = SceneController.getInstance();

    void execute();
}
