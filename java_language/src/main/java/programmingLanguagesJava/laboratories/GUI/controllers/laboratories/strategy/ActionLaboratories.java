package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategy;

import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;

/**
 * Интерфейс, который связывает элементы вызова элементов UI c помощью паттерна "Стратегия".
 * В данном случае он для элементов окна с лабораторными работами
 */
public interface ActionLaboratories {
    ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    SceneController controller = SceneController.getInstance();
    ComboboxConfigurator comboboxConfigurator = ComboboxConfigurator.getInstance();

    void execute();
}
