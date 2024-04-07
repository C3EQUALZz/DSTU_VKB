package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.scene.control.Button;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class AddHumanButtonActionViewingDatabase implements ActionViewingDatabase {

    private final Button addHumanButton;

    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(addHumanButton, event -> controller.switchFromDataBaseViewToFillingForm());
    }

}
