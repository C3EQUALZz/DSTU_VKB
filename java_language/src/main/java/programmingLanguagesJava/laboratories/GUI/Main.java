package programmingLanguagesJava.laboratories.GUI;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

import java.io.File;

import java.io.IOException;
import java.util.Objects;

public class Main extends Application {
    protected Stage primaryStage;

    /**
     * Данный класс является точкой входа в нашу программу, здесь происходит запуск приложения
     *
     * @param stage сущность нашего приложения
     */
    @Override
    public void start(Stage stage) throws IOException {
        this.primaryStage = stage;
        initStage();

        Parent menuFile = FXMLLoader.load(Objects.requireNonNull(getClass().getResource("/menuFiles/menu.fxml")));
        Scene menu = new Scene(menuFile);
        this.primaryStage.setScene(menu);
        this.primaryStage.show();

    }

    /**
     * Установка параметров на все приложение (название, неизменяемость по размеру,
     */
    private void initStage() {
        this.primaryStage.setTitle("Ковалев Данил ВКБ22");
        this.primaryStage.setResizable(false);
        var imageStage = new Image("/menuFiles/desktop.png");
        this.primaryStage.getIcons().add(imageStage);
    }

}
