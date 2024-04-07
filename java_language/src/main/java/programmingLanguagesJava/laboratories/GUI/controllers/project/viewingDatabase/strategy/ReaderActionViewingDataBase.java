package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readersFromDatabase.readingDocxFromDatabase.Reader;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;
import lombok.RequiredArgsConstructor;

/**
 * Конфигурация считывания файла при нажатии на кнопку.
 */
@RequiredArgsConstructor
public class ReaderActionViewingDataBase implements ActionViewingDatabase {

    private final TableViewContext context;
    private final Button button;

    /**
     * Точка запуска данного метода
     */
    @Override
    public void execute() {
        new Reader(context.customersTableView(), button).event();
    }
}
