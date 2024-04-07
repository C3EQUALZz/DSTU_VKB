package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readingDocxFromDatabase.Reader;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.strategyContext.TableViewContext;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class ReaderActionViewingDataBase implements ActionViewingDatabase {

    private final TableViewContext context;
    private final Button button;

    @Override
    public void execute() {
        new Reader(context.customersTableView(), button).event();
    }
}
