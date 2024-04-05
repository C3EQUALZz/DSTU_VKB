package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;

public interface ActionFillingForm {

    ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    SceneController controller = SceneController.getInstance();
    ComboboxConfigurator comboboxConfigurator = ComboboxConfigurator.getInstance();

    void execute();

}
