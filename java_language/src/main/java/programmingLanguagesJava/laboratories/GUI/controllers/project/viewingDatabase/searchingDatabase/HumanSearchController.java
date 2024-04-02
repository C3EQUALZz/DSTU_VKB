package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase;

import javafx.collections.transformation.FilteredList;
import javafx.collections.transformation.SortedList;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import lombok.Builder;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.searchingDatabase.strategy.SearchStrategy;

import java.util.List;

@Builder
public class HumanSearchController implements ElementDatabaseView {

    private final TableView<PersonInfo> customersTableView;
    private final FilteredList<PersonInfo> filteredData;
    private final TextField keywordTextField;
    private final List<SearchStrategy> searchStrategies;

    @Override
    public void event() {
        keywordTextField.textProperty().addListener((observable, oldValue, newValue) ->
                filteredData.setPredicate(personInfo -> {

            if (newValue.isEmpty() || newValue.isBlank()) {
                return true;
            }

            return searchStrategies.stream().anyMatch(strategy -> strategy.matches(personInfo, newValue));
        }));

        SortedList<PersonInfo> sortedData = new SortedList<>(filteredData);
        sortedData.comparatorProperty().bind(customersTableView.comparatorProperty());
        customersTableView.setItems(sortedData);
    }


}
