package programmingLanguagesJava.laboratories.GUI.controllers.projectControllers;

import com.sothawo.mapjfx.Coordinate;
import com.sothawo.mapjfx.MapView;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import java.net.URL;
import java.util.ResourceBundle;

public class MenuAddress implements Initializable {

    @FXML
    private MapView mapView;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        mapView.initialize();
        // Установка начальных координат и масштаба
        mapView.setCenter(new Coordinate(47.2371576587879, 39.711658338598745));
        mapView.setZoom(17);
    }
}
