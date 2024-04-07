package programmingLanguagesJava.laboratories.GUI.config;

import javafx.scene.image.Image;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

/**
 * Класс, который позволяет конфигурировать отдельный stage под мои требования.
 */
public class StageConfigurator {

    /**
     * Метод, который и производит настройку всего
     * @param primaryStage Stage, который мы хотим настроить
     * @return отформатированный Stage
     */
     public static Stage configureStage(Stage primaryStage) {
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
