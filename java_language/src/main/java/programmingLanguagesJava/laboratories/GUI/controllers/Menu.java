package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.text.Text;

import java.net.URL;
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

    }

    private void ButtonMouseEvent() {

    }
}
