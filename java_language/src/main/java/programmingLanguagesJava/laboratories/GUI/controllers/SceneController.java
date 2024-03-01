/**
 * SceneController - это мой класс, который управляет другими контроллерами.
 * Был создан для того, чтобы можно было удобно переключаться между окнами.
 * Здесь реализован удобный интерфейс, чтобы переключаться между окнами.
 */

package programmingLanguagesJava.laboratories.GUI.controllers;


import javafx.animation.FadeTransition;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.scene.input.MouseEvent;
import javafx.util.Duration;

import java.io.IOException;
import java.util.Objects;

public class SceneController {
    // Параметры для определения координат мышки
    private double xOffset = 0, yOffset = 0;
    // Наш Stage, с которым мы хотим взаимодействовать
    private Stage stage;
    // В данном приложении будет 3 окна, вот как раз они ниже
    private Scene menu, laboratories, project;
    // Костыль, который проверяет, что окна были созданы. Сделано с целью того, чтобы каждый раз не пересоздавать окно
    private boolean flagWindowCreated;
    private static SceneController instance;

    public SceneController(Stage stage) {
        this.stage = stage;
    }

    public static SceneController getInstance(Stage stage) {
        if (instance == null) {
            instance = new SceneController(stage);
        }
        return instance;
    }

    public SceneController() {
    }

    /**
     * Переключение с меню на лабораторные
     *
     * @param event MouseEvent, с помощью которого мы будем определять в каком Stage это происходит
     * @throws IOException может броситься такая ошибка, так как считывает файлы.
     */
    public void switchFromMenuToLaboratories(MouseEvent event) throws IOException {

        if (!flagWindowCreated) {
            createAllScenes(event);
        }

        animationSlideWindow(laboratories);
    }

    /**
     * Переключение с меню на проект
     *
     * @param event MouseEvent, с помощью которого мы будем определять в каком Stage это происходит
     * @throws IOException может броситься такая ошибка, так как считывает файлы
     */
    public void switchFromMenuToProject(MouseEvent event) throws IOException {

        if (!flagWindowCreated) {
            createAllScenes(event);
        }

        animationSlideWindow(this.project);
    }

    /**
     * Переключение с любого окна на меню
     *
     * @param event MouseEvent, с помощью которого мы будем определять в каком Stage это происходит
     * @throws IOException может броситься такая ошибка, так как считывает файлы
     */
    public void switchToMenu(MouseEvent event) throws IOException {

        if (!flagWindowCreated) {
            createAllScenes(event);
        }

        animationSlideWindow(this.menu);
    }

    /**
     * Переключение с любого окна на меню.
     * Здесь используется для удобства взаимодействия с самого начала приложения.
     * При первом запуске
     * @throws IOException может броситься такая ошибка, так как считывает файлы
     */
    public void switchToMenu() throws IOException {

        if (!flagWindowCreated) {
            this.menu = createWindow();
        }

        this.stage.setScene(this.menu);
    }

    /**
     * Метод, который создает все окна сразу, чтобы каждый раз отдельное окно не подгружать в память
     * Такой способ увеличивает быстродействие приложения, но больше расходуется память
     * @param event MouseEvent, с помощью которого мы будем определять в каком Stage это происходит
     */
    private void createAllScenes(MouseEvent event) {

        try {
            this.menu = createWindow("/menuFiles/menu.fxml", event);
            this.laboratories = createWindow("/laboratoriesFiles/laboratories.fxml", event);
            this.project = createWindow("/projectFiles/project.fxml", event);

        } catch (IOException e) {
            throw new RuntimeException("Неправильные файлы или event");
        }

        this.flagWindowCreated = true;
    }


    /**
     * @param filePath Путь к файлу
     * @param event MouseEvent, с помощью которого мы будем определять в каком Stage это происходит
     * @return Возвращает созданную сцену
     * @throws IOException может возникнуть ошибка при считывании файла с FXML
     */
    private Scene createWindow(String filePath, MouseEvent event) throws IOException {
        Parent windowFXML = FXMLLoader.load(Objects.requireNonNull(getClass().getResource(filePath)));
        var scene = new Scene(windowFXML);

        stage = (Stage) ((Node) event.getSource()).getScene().getWindow();

        // Возможность, чтобы окно могло передвигаться при зажатии мышки
        windowFXML.setOnMousePressed(ev -> {
            xOffset = ev.getSceneX();
            yOffset = ev.getSceneY();
        });

        windowFXML.setOnMouseDragged(ev -> {
            stage.setX(ev.getScreenX() - xOffset);
            stage.setY(ev.getScreenY() - yOffset);
        });

        // Костыль, чтобы не было углов у приложения, которые видны в SceneBuilder
        scene.setFill(Color.TRANSPARENT);

        return scene;
    }

    private Scene createWindow() throws IOException {

        Parent windowFXML = FXMLLoader.load(Objects.requireNonNull(getClass().getResource("/menuFiles/menu.fxml")));

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


        var scene = new Scene(windowFXML);

        // Костыль, чтобы не было углов у приложения, которые видны в SceneBuilder
        scene.setFill(Color.TRANSPARENT);

        return scene;
    }

    /**
     * Метод, чтобы была анимация переключения между окнами приложения.
     * @param scene окно, на которое мы хотим переключиться.
     */
    private void animationSlideWindow(Scene scene) {
        FadeTransition fadeOut = new FadeTransition(Duration.millis(750), this.stage.getScene().getRoot());
        fadeOut.setFromValue(1.0);
        fadeOut.setToValue(0.0);

        fadeOut.setOnFinished(e -> {
            FadeTransition fadeIn = new FadeTransition(Duration.millis(700), scene.getRoot());
            fadeIn.setFromValue(0.0);
            fadeIn.setToValue(1.0);
            fadeIn.play();
            this.stage.setScene(scene);
        });

        fadeOut.play();
    }
}
