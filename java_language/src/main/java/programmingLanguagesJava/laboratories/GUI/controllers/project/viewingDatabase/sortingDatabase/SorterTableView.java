package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.sortingDatabase;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.RadioButton;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;

import java.util.Comparator;
import java.util.function.Function;

/**
 * Класс, который сортирует таблицу динамически в зависимости от нажатой кнопки.
 */
@RequiredArgsConstructor
public class SorterTableView implements ElementDatabaseView {

    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();
    private final RadioButton lastNameRadioButton, firstNameRadioButton, patronymicRadioButton;
    private final ObservableList<PersonInfo> personInfoList;

    /**
     * Метод event() настраивает обработчики событий для радиокнопок.
     * Когда выбрана радиокнопка, данные в TableView сортируются по соответствующему полю.
     */
    @Override
    public void event() {
        setupSortingRadioButton(lastNameRadioButton, personInfoList, PersonInfo::getLastName);
        setupSortingRadioButton(firstNameRadioButton, personInfoList, PersonInfo::getFirstName);
        setupSortingRadioButton(patronymicRadioButton, personInfoList, PersonInfo::getPatronymic);
    }

    /**
     * Метод настраивает обработчик событий для указанной радиокнопки.
     * Когда радиокнопка выбрана, данные сортируются по значению, извлеченному с помощью valueExtractor.
     */
    private void setupSortingRadioButton(RadioButton radioButton,
                                         ObservableList<PersonInfo> data,
                                         Function<PersonInfo, String> valueExtractor) {

        buttonConfigurator.setupButtonEvent(
                radioButton,
                event -> FXCollections.sort(data, Comparator.comparing(valueExtractor, String.CASE_INSENSITIVE_ORDER))
        );
    }



}
