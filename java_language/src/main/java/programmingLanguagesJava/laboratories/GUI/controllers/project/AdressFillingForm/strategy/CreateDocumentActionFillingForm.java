package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.strategy;

import javafx.application.Platform;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.NotificationClass;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing.DocxProcessor;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.fileChooserInteraction.FileChooserController;
import lombok.RequiredArgsConstructor;

import java.util.Map;

@RequiredArgsConstructor
public class CreateDocumentActionFillingForm implements ActionFillingForm {

    private final FileChooserController fileChooserController;
    private final Map<String, String> jsonData;
    private final Button createDocument;
    private final TextField addressField;
    private final ComboBox<String> combobox;


    @Override
    public void execute() {
        Platform.runLater(() -> {
            var docxProcessor = new DocxProcessor(jsonData);
            buttonConfigurator.setupButtonEvent(createDocument, event -> {
                jsonData.put("addressField", addressField.getText());
                jsonData.put("mainPerson", combobox.getValue());
                jsonData.put("buildingPlan", fileChooserController.getSelectedFile());
                jsonData.put("allPeople", String.join(", ", combobox.getItems()));
                jsonData.put("pathToFile", docxProcessor.event());
                new NotificationClass().start();
            });
        });

    }
}
