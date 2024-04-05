package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.DataBaseSQLite;
import lombok.RequiredArgsConstructor;
import java.util.HashMap;

@RequiredArgsConstructor
public class AddDataToDatabaseActionFillingForm implements ActionFillingForm {

    private final Button addDataToDB;
    private final HashMap<String, String> jsonData;
    private final DataBaseSQLite dataBaseSQLite = DataBaseSQLite.getInstance();

    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(addDataToDB, event -> dataBaseSQLite.insert(jsonData));
    }

}
