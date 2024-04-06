package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.addingNames.TextFieldAddController;

public class TextFieldAddControllerActionFillingForm implements ActionFillingForm {

    private final TextFieldAddController textFieldAddController;
    private final Button addHuman;
    private final ComboBox<String> combobox;

    public TextFieldAddControllerActionFillingForm(TextField textField, Button button, ComboBox<String> combobox) {
        this.textFieldAddController = new TextFieldAddController(textField);
        this.addHuman = button;
        this.combobox = combobox;
        comboboxConfigurator.defaultConfiguration(combobox);
    }

    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(addHuman, event -> {
            textFieldAddController.event();
            comboboxConfigurator.setupComboboxEvent(combobox, textFieldAddController.getPersons());
        });
    }

}
