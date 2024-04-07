package programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver;

import javafx.application.Platform;
import javafx.geometry.Pos;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.controlsfx.control.Notifications;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.DataBaseSQLite;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;

import java.util.Random;

class AlertService extends Thread {

    private final Stage stage = SceneController.getInstance().getStage();
    private final PersonInfo personInfo = DataBaseSQLite.getInstance().loadPersonInfos().get(new Random().nextInt(0, 10));

    @Override
    public void run() {

        var text = String.format(
                "Произошла кража! У '%s'. Полиция уведомлена! Вызван ближайший наряд охраны!",
                String.join(" ", personInfo.getLastName(), personInfo.getFirstName(), personInfo.getPatronymic())
        );

        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            throw new RuntimeException("Поток для уведомления о краже был прерван", e);
        }

        var notification = Notifications.create()
                .title("Операция произошла успешно")
                .owner(stage)
                .text(text)
                .hideAfter(Duration.seconds(7))
                .position(Pos.TOP_CENTER);

        Platform.runLater(notification::showWarning);
    }

}
