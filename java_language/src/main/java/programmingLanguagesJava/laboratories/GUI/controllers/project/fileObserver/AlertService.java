package programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Dialog;
import javafx.scene.paint.Color;
import javafx.stage.Modality;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.IOException;
import java.util.Objects;

public class AlertService {
    private static AlertService instance;
    private Dialog<Void> alert;

    private AlertService() {}

    public static AlertService getInstance() {
        if (instance == null) {
            instance = new AlertService();
        }
        return instance;
    }

    public void createAlert() {
        if (alert == null || !alert.isShowing()) {
            try {
                var scene = new Scene(loadFXML());
                scene.setFill(Color.TRANSPARENT);

                alert = new Dialog<>();
                alert.initModality(Modality.APPLICATION_MODAL);

                Stage stage = (Stage) alert.getDialogPane().getScene().getWindow();
                stage.initStyle(StageStyle.TRANSPARENT);
                stage.setScene(scene);

                stage.showAndWait();

            } catch (IOException e) {
                throw new RuntimeException("Не получилось считать файл", e);
            }
        }
    }

    private Parent loadFXML() throws IOException {
        return FXMLLoader.load(Objects.requireNonNull(getClass().getResource("/projectFiles/modal-window.fxml")));
    }
}
