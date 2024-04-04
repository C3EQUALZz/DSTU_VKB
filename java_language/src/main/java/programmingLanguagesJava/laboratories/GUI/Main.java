/*
 * Точка запуска программы, здесь создаются окна нашего приложения (Scene) и происходит конфигурация приложения (Stage)
 */

package programmingLanguagesJava.laboratories.GUI;

import javafx.application.Application;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;

public class Main extends Application {

    /**
     * Данный класс является точкой входа в нашу программу, здесь происходит запуск приложения
     *
     * @param stage сущность нашего приложения.
     */
    @Override
    public void start(Stage stage) {
        var stageInitialized = initStage(stage);
        var controller = SceneController.getInstance(stage);
        controller.setStartMenu();
        stageInitialized.show();
    }

    /**
     * Установка параметров на все приложение
     */
    private Stage initStage(Stage primaryStage) {
        // Название приложения
        primaryStage.setTitle("Ковалев Данил ВКБ22");

        // Установка неизменяемости по размеру, так как я немного криво располагаю элементы.
        // Не умею в масштабируемое приложение, поэтому так.
        primaryStage.setResizable(false);

        // Установка изображения для приложения
        primaryStage.getIcons().add(new Image("/menuFiles/images/desktop.png"));

        // Определяю так, чтобы не было системных Windows компонентов, так как с ними выглядит ужасно.
        primaryStage.initStyle(StageStyle.TRANSPARENT);

        return primaryStage;
    }
}