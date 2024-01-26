package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.animation.AnimationTimer;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.text.Text;

import java.net.URL;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ResourceBundle;

public class Menu implements Initializable {
    @FXML
    private Button ButtonLabs;

    @FXML
    private Button ButtonProject;

    @FXML
    private Text MinutesTimer;

    @FXML
    private Text SecondsTimer;

    @FXML
    private Text hoursTimer;


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        clock();

    }

    private void ButtonMouseEvent() {

    }

    private void clock() {
        AnimationTimer timer = new AnimationTimer() {
            @Override
            public void handle(long now) {
                Platform.runLater(() -> {
                    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");
                    MinutesTimer.setText(LocalDateTime.now().format(formatter).substring(3, 5));
                    SecondsTimer.setText(LocalDateTime.now().format(formatter).substring(6, 8));
                    hoursTimer.setText(LocalDateTime.now().format(formatter).substring(0, 2));
                });
            }
        };
        timer.start();
    }
}
