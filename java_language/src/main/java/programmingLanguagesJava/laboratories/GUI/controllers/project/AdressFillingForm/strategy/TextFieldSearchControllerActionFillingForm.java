package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import javafx.scene.control.Button;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.searchEngineField.TextFieldSearchController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategyContext.StrategyContextMap;

public class TextFieldSearchControllerActionFillingForm implements ActionFillingForm {

    private final TextFieldSearchController textFieldSearchController;
    private final Button startSearch;

    public TextFieldSearchControllerActionFillingForm(StrategyContextMap strategyContextMap, Button startSearch) {
        this.textFieldSearchController = new TextFieldSearchController(strategyContextMap.mapView(), strategyContextMap.adressTextField());
        this.startSearch = startSearch;
    }

    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(startSearch, event -> textFieldSearchController.event());
    }

}
