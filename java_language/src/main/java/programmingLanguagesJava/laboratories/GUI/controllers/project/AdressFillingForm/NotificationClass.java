/**
 * Видео гайд по данной библиотеке: https://youtu.be/occdZWprRjg?si=8TspM0l5kgm1Dk-x
 * Здесь говорится насчет CSS настройки: https://stackoverflow.com/questions/44710401/is-there-a-way-to-change-the-built-in-controlfx-notification-popup-color
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import javafx.application.Platform;
import javafx.geometry.Pos;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.controlsfx.control.Notifications;
import lombok.RequiredArgsConstructor;
import java.util.Objects;

/**
 * Класс, который нужен для создания уведомления.
 */
@RequiredArgsConstructor
public class NotificationClass extends Thread {

    private static final Image image = new Image(Objects.requireNonNull(NotificationClass.class.getResourceAsStream("/projectFiles/images/verified.png")));
    private final Stage stage;

    @Override
    public void run() {

        // Здесь стоит костыль, чтобы эмулировать реальное ожидание конца.
        // В любом кайфе это сработает, потому что у меня максимально стабильный парсер.
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            throw new RuntimeException("Поток для уведомления был прерван", e);
        }

        var notification = Notifications.create()
                .title("Операция произошла успешно")
                .owner(stage)
                .text("Документ был создан! Сохраните в базу данных! ")
                .hideAfter(Duration.seconds(7))
                .graphic(new ImageView(image))
                .position(Pos.TOP_CENTER);

        Platform.runLater(notification::show);
    }
}
