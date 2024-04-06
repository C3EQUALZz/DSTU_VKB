package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.DataBaseSQLite;
import lombok.RequiredArgsConstructor;

import java.util.Map;

/**
 * Класс, который конфигурирует кнопку добавления в базу данных.
 */
@RequiredArgsConstructor
public class AddDataToDatabaseActionFillingForm implements ActionFillingForm {

    private final Map<String, String> jsonData;
    private final Button addDataToDB;

    /**
     * Точка запуска
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(addDataToDB, event -> DataBaseSQLite.getInstance().insert(jsonData));
    }

}
