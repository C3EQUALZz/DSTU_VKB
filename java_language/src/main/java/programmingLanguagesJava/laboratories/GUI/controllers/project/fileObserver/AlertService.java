package programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver;

import javafx.scene.control.Dialog;
import javafx.stage.Modality;
import javafx.stage.Stage;
import programmingLanguagesJava.laboratories.GUI.config.SceneConfigurator;
import programmingLanguagesJava.laboratories.GUI.config.StageConfigurator;

import java.io.IOException;

class AlertService {
    private static AlertService instance;

    private Dialog<Void> alert;

    private AlertService() {}

    static AlertService getInstance() {
        if (instance == null) {
            instance = new AlertService();
        }
        return instance;
    }

    void createAlert() {
        if (alert == null || !alert.isShowing()) {
            try {

                alert = new Dialog<>();
                alert.initModality(Modality.APPLICATION_MODAL);

                var scene = SceneConfigurator.createScene("/projectFiles/modal-window.fxml");
                var stage = StageConfigurator.configureStage((Stage) alert.getDialogPane().getScene().getWindow());

                stage.setScene(scene);
                stage.showAndWait();

            } catch (IOException e) {
                throw new RuntimeException("Не получилось считать файл", e);
            }
        }
    }

}
