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
import java.util.Stack;

public class SceneController {
    private double xOffset = 0, yOffset = 0;
    private final Stage stage;
    private static SceneController instance;
    private final Stack<Scene> sceneHistory = new Stack<>();

    private enum Scenes {
        ;
        private static Scene MENU = null;
        private static Scene LABORATORIES = null;
        private static Scene PROJECT_MENU = null;
        private static Scene PROJECT_FILLING_FORM = null;
        private static Scene PROJECT_DATABASE_VIEW = null;
    }

    private enum ScenePath {
        ;
        private static final String MENU_FXML_PATH = "/menuFiles/menu.fxml";
        private static final String LABORATORIES_FXML_PATH = "/laboratoriesFiles/laboratories.fxml";
        private static final String MENU_PROJECT_FXML_PATH = "/projectFiles/menu_project.fxml";
        private static final String FILLING_FORM_PROJECT_FXML_PATH = "/projectFiles/project.fxml";
        private static final String DATABASE_VIEW_PROJECT_FXML_PATH = "/projectFiles/database_project.fxml";
    }

    /**
     * Конструктор сделал приватным, чтобы реализовать Singleton - гугл в помощь
     * @param stage окно Stage, к которому мы хотим прикрепить наш SceneController
     */
    private SceneController(Stage stage) {
        this.stage = stage;
    }

    /**
     * Данный метод как раз и есть реализация паттерна Singleton на Java. Тут нет метода __new__, как в Python, чтобы
     * работать не зная действие под капотом.
     * @param stage окно Stage, к которому мы хотим прикрепить наш SceneController
     * @return возвращает SceneController
     */
    public static SceneController getInstance(Stage stage) {
        if (instance == null) {
            instance = new SceneController(stage);
        }
        return instance;
    }

    /**
     * Метод больше как костыль, потому что в
     * @return SceneController, который используется в BaseController.
     */
    public static SceneController getInstance() {
        if (instance == null) {
            throw new IllegalStateException("SceneController не был инициализирован");
        }
        return instance;
    }

    /**
     * Переключение с меню на лабораторные работы
     */
    public void switchFromMenuToLaboratories() {
        animationSlideWindow(Scenes.LABORATORIES);
        sceneHistory.push(Scenes.MENU);
    }

    /**
     * Переключение с меню на проект
     */
    public void switchToMenuProject() {
        animationSlideWindow(Scenes.PROJECT_MENU);
        sceneHistory.push(Scenes.MENU);
    }

    /**
     * Переключение с меню проекта на окно с записью информации о заказчике в БД
     */
    public void switchFromMenuProjectToFillingForm() {
        animationSlideWindow(Scenes.PROJECT_FILLING_FORM);

        if (!sceneHistory.peek().equals(Scenes.PROJECT_MENU)) {
            sceneHistory.push(Scenes.PROJECT_MENU);
        }

    }

    /**
     * Переключение с меню на просмотр базы данных. Здесь стоит условие if, чтобы не забили стек
     */
    public void switchFromMenuProjectToDataBaseView() {
        animationSlideWindow(Scenes.PROJECT_DATABASE_VIEW);

        if (!sceneHistory.peek().equals(Scenes.PROJECT_MENU)) {
            sceneHistory.push(Scenes.PROJECT_MENU);
        }

    }

    /**
     * Метод, который переключает на окно с заполнениями формы
     */
    public void switchFromDataBaseViewToFillingForm() {
        animationSlideWindow(Scenes.PROJECT_FILLING_FORM);
        sceneHistory.push(Scenes.PROJECT_DATABASE_VIEW);
    }

    /**
     * Метод, который возвращает на прошлое окно.
     */
    public void goBack() {
        if (!sceneHistory.isEmpty()) {
            animationSlideWindow(sceneHistory.pop());
        }
    }

    /**
     * Переключение с любого окна на меню.
     * Здесь используется для удобства взаимодействия с самого начала приложения.
     * При первом запуске
     */
    public void setStartMenu() {

        try {

            Scenes.MENU = createWindow(ScenePath.MENU_FXML_PATH);
            Scenes.LABORATORIES = createWindow(ScenePath.LABORATORIES_FXML_PATH);
            Scenes.PROJECT_MENU = createWindow(ScenePath.MENU_PROJECT_FXML_PATH);
            Scenes.PROJECT_FILLING_FORM = createWindow(ScenePath.FILLING_FORM_PROJECT_FXML_PATH);
            Scenes.PROJECT_DATABASE_VIEW = createWindow(ScenePath.DATABASE_VIEW_PROJECT_FXML_PATH);

        } catch (IOException e) {

            throw new RuntimeException("Неправильные файлы или event");

        }
        sceneHistory.push(Scenes.MENU);
        this.stage.setScene(sceneHistory.peek());
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

    /**
     * Метод, который нужен, чтобы можно было передвигать окно
     * @param windowFXML окно, которое мы хотим перетаскивать
     */
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
            var fadeIn = new FadeTransition(Duration.millis(850), scene.getRoot());
            fadeIn.setFromValue(0.0);
            fadeIn.setToValue(1.0);
            fadeIn.play();
            this.stage.setScene(scene);
        });

        fadeOut.play();
    }
}