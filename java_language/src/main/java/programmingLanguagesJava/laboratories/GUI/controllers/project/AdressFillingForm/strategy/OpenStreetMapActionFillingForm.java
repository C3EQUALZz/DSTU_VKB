package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;


import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.processingEventsOnMap.OpenStreetMap;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategyContext.StrategyContextMap;

public class OpenStreetMapActionFillingForm implements ActionFillingForm {

    private final OpenStreetMap openStreetMap;

    public OpenStreetMapActionFillingForm(StrategyContextMap strategyContextMap) {
        this.openStreetMap = new OpenStreetMap(strategyContextMap.mapView(), strategyContextMap.adressTextField());
    }

    @Override
    public void execute() {
        this.openStreetMap.event();
    }

}
