/**
 * SceneController - это мой класс, который управляет другими контроллерами.
 * Был создан для того, чтобы можно было удобно переключаться между окнами.
 * Здесь реализован удобный интерфейс, чтобы переключаться между окнами.
 */

package programmingLanguagesJava.laboratories.GUI.controllers;


import javafx.animation.FadeTransition;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.io.IOException;
import java.util.Objects;

public class SceneController {
    private double xOffset = 0, yOffset = 0;
    private final Stage stage;
    private static SceneController instance;

    private enum Scenes {
        ;
        private static Scene MENU = null;
        private static Scene LABORATORIES = null;
        private static Scene PROJECT = null;
    }

    private enum ScenePath {
        ;
        private static final String MENU_FXML_PATH = "/menuFiles/menu.fxml";
        private static final String LABORATORIES_FXML_PATH = "/laboratoriesFiles/laboratories.fxml";
        private static final String PROJECT_FXML_PATH = "/projectFiles/project.fxml";
    }


    private SceneController(Stage stage) {
        this.stage = stage;
    }

    public static SceneController getInstance(Stage stage) {
        if (instance == null) {
            instance = new SceneController(stage);
        }
        return instance;
    }

    public static SceneController getInstance() {
        if (instance == null) {
            throw new IllegalStateException("SceneController не был инициализирован");
        }
        return instance;
    }

    /**
     * Переключение с меню на лабораторные
     *
     * @throws IOException может броситься такая ошибка, так как считывает файлы.
     */
    public void switchFromMenuToLaboratories() throws IOException {
        animationSlideWindow(Scenes.LABORATORIES);
    }

    /**
     * Переключение с меню на проект
     *
     * @throws IOException может броситься такая ошибка, так как считывает файлы
     */
    public void switchFromMenuToProject() throws IOException {
        animationSlideWindow(Scenes.PROJECT);
    }

    /**
     * Переключение с любого окна на меню
     *
     * @throws IOException может броситься такая ошибка, так как считывает файлы
     */
    public void switchToMenu() throws IOException {
        animationSlideWindow(Scenes.MENU);
    }

    /**
     * Переключение с любого окна на меню.
     * Здесь используется для удобства взаимодействия с самого начала приложения.
     * При первом запуске
     * @throws IOException может броситься такая ошибка, так как считывает файлы
     */
    public void setStartMenu() throws IOException {

        try {

            Scenes.MENU = createWindow(ScenePath.MENU_FXML_PATH);
            Scenes.LABORATORIES = createWindow(ScenePath.LABORATORIES_FXML_PATH);
            Scenes.PROJECT = createWindow(ScenePath.PROJECT_FXML_PATH);

        } catch (IOException e) {

            throw new RuntimeException("Неправильные файлы или event");

        }

        this.stage.setScene(Scenes.MENU = createWindow(ScenePath.MENU_FXML_PATH));
    }


    /**
     * @param filePath Путь к файлу
     * @return Возвращает созданную сцену
     * @throws IOException может возникнуть ошибка при считывании файла с FXML
     */
    private Scene createWindow(String filePath) throws IOException {
        try {

            Parent windowFXML = FXMLLoader.load(Objects.requireNonNull(getClass().getResource(filePath)));
            var scene = new Scene(windowFXML);
            setWindowDragged(windowFXML);
            // Костыль, чтобы не было углов у приложения, которые видны в SceneBuilder
            scene.setFill(Color.TRANSPARENT);

            return scene;

        } catch (IOException e) {

            throw new RuntimeException("Не смог загрузить файл: " + filePath, e);

        }

    }

    private void setWindowDragged(Parent windowFXML) {
        // Возможность, чтобы окно могло передвигаться при зажатии мышки
        windowFXML.setOnMousePressed(ev -> {
            xOffset = ev.getSceneX();
            yOffset = ev.getSceneY();
        });

        // Когда зажатое окно
        windowFXML.setOnMouseDragged(ev -> {
            this.stage.setX(ev.getScreenX() - xOffset);
            this.stage.setY(ev.getScreenY() - yOffset);
        });
    }

    /**
     * Метод, чтобы была анимация переключения между окнами приложения.
     * @param scene окно, на которое мы хотим переключиться.
     */
    private void animationSlideWindow(Scene scene) {
        var fadeOut = new FadeTransition(Duration.millis(750), this.stage.getScene().getRoot());
        fadeOut.setFromValue(1.0);
        fadeOut.setToValue(0.0);

        fadeOut.setOnFinished(e -> {
            var fadeIn = new FadeTransition(Duration.millis(700), scene.getRoot());
            fadeIn.setFromValue(0.0);
            fadeIn.setToValue(1.0);
            fadeIn.play();
            this.stage.setScene(scene);
        });

        fadeOut.play();
    }
}