package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.sortingDatabase;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.RadioButton;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import lombok.Builder;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;

import java.util.Comparator;
import java.util.function.Function;

@Builder
public class SorterTableView implements ElementDatabaseView {

    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    private RadioButton lastNameRadioButton, firstNameRadioButton, patronymicRadioButton;
    private ObservableList<PersonInfo> data;


    @Override
    public void event() {
        setupSortingRadioButton(lastNameRadioButton, data, PersonInfo::getLastName);
        setupSortingRadioButton(firstNameRadioButton, data, PersonInfo::getFirstName);
        setupSortingRadioButton(patronymicRadioButton, data, PersonInfo::getPatronymic);
    }

    private void setupSortingRadioButton(RadioButton radioButton, ObservableList<PersonInfo> data, Function<PersonInfo, String> valueExtractor) {
        buttonConfigurator.setupButtonEvent(radioButton, event -> FXCollections.sort(data, Comparator.comparing(valueExtractor, String.CASE_INSENSITIVE_ORDER)));
    }

}
