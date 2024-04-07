package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;

public interface ActionViewingDatabase {

    ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    SceneController controller = SceneController.getInstance();

    void execute();
}
