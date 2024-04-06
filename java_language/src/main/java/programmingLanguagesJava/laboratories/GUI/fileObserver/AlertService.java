package programmingLanguagesJava.laboratories.GUI.fileObserver;

import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.Modality;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.IOException;
import java.util.Objects;

public class AlertService {

    private Stage alertStage;

    public void createAlert() {
        try {
            if (alertStage == null) {

                Parent root = FXMLLoader.load(Objects.requireNonNull(getClass().getResource("/projectFiles/modal-window.fxml")));
                var scene = new Scene(root);

                scene.setFill(Color.TRANSPARENT);

                alertStage = new Stage();
                alertStage.initStyle(StageStyle.TRANSPARENT);

                alertStage.setScene(scene);
                alertStage.initModality(Modality.APPLICATION_MODAL);
            }

            if (!alertStage.isShowing()) {
                Platform.runLater(alertStage::show);
            }

        } catch (IOException e) {
            throw new RuntimeException("Не получилось загрузить файл с уведомлением", e);
        }
    }
}
