package programmingLanguagesJava.laboratories.GUI;

import javafx.application.Application;
import javafx.scene.image.Image;
import javafx.stage.Stage;

public class Main extends Application {
    protected Stage primaryStage;

    /**
     * Данный класс является точкой входа в нашу программу, здесь происходит запуск приложения
     *
     * @param stage сущность нашего приложения
     */
    @Override
    public void start(Stage stage) {
        this.primaryStage = stage;
        this.primaryStage.setTitle("Ковалев Данил ВКБ22");
        this.primaryStage.getIcons().add(new Image("photos/desktop.png"));


    }

}
