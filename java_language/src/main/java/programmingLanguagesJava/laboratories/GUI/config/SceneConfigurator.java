package programmingLanguagesJava.laboratories.GUI.config;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Objects;

/**
 * Класс, который нужен, чтобы настраивать Scene.
 */
public class SceneConfigurator {

    private static final String CSS = Objects.requireNonNull(SceneConfigurator.class.getResource("/stageFiles/Styles.css")).toExternalForm();

    private static double xOffset = 0, yOffset = 0;

    /**
     * Метод, который нужен, чтобы можно было передвигать окно
     *
     * @param windowFXML окно, которое мы хотим перетаскивать
     */
    private static void setWindowDragged(Stage stage, Parent windowFXML) {
        // Возможность, чтобы окно могло передвигаться при зажатии мышки
        windowFXML.setOnMousePressed(ev -> {
            xOffset = ev.getSceneX();
            yOffset = ev.getSceneY();
        });

        // Когда зажатое окно
        windowFXML.setOnMouseDragged(ev -> {
            stage.setX(ev.getScreenX() - xOffset);
            stage.setY(ev.getScreenY() - yOffset);
        });
    }

    /**
     * @param filePath Путь к файлу
     * @return Возвращает созданную сцену
     */
    public static Scene createScene(String filePath) throws IOException {
        Parent windowFXML = FXMLLoader.load(Objects.requireNonNull(SceneConfigurator.class.getResource(filePath)));

        var scene = new Scene(windowFXML);

        setWindowDragged((Stage) scene.getWindow(), windowFXML);

        // Костыль, чтобы не было углов у приложения, которые видны в SceneBuilder
        scene.setFill(Color.TRANSPARENT);

        scene.getStylesheets().add(CSS);

        return scene;

    }

}
