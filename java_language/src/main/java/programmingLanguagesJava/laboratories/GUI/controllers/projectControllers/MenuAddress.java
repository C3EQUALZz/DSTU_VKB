package programmingLanguagesJava.laboratories.GUI.controllers.projectControllers;

import com.dlsc.gmapsfx.GoogleMapView;
import com.dlsc.gmapsfx.MapComponentInitializedListener;
import com.dlsc.gmapsfx.javascript.object.GoogleMap;
import com.dlsc.gmapsfx.javascript.object.LatLong;
import com.dlsc.gmapsfx.javascript.object.MapOptions;
import com.dlsc.gmapsfx.javascript.object.MapTypeIdEnum;
import com.dlsc.gmapsfx.service.geocoding.GeocoderStatus;
import com.dlsc.gmapsfx.service.geocoding.GeocodingResult;
import com.dlsc.gmapsfx.service.geocoding.GeocodingService;
import javafx.animation.PauseTransition;
import javafx.application.Platform;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.util.Duration;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.SceneController;


import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public class MenuAddress implements Initializable, MapComponentInitializedListener {

    @FXML
    private GoogleMapView googleMapView;

    @FXML
    private TextField addressTextField;
    @FXML private Button backButton, exitButton;

    private GoogleMap map;

    private GeocodingService geocodingService;
    private final ButtonConfigurator buttonConfigurator = new ButtonConfigurator();
    private final SceneController controller = new SceneController();

    private final StringProperty address = new SimpleStringProperty();


    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {

        addressTextField.setOnAction(this::addressTextFieldAction);

        buttonConfigurator.setupButtonEvent(backButton, event -> {

            try {
                controller.switchToMenu(event);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }

        });

        buttonConfigurator.setupButtonEvent(exitButton, event -> {

            PauseTransition pause = new PauseTransition(Duration.millis(100));
            pause.setOnFinished(evt -> Platform.exit());
            pause.play();

        });

        googleMapView.addMapInitializedListener(this);
        address.bind(addressTextField.textProperty());
    }

    @Override
    public void mapInitialized() {
        geocodingService = new GeocodingService();
        MapOptions mapOptions = new MapOptions();

        mapOptions.center(new LatLong(47.6097, -122.3331))
                .mapType(MapTypeIdEnum.ROADMAP)
                .overviewMapControl(false)
                .panControl(false)
                .rotateControl(false)
                .scaleControl(false)
                .streetViewControl(false)
                .zoomControl(false)
                .zoom(12);

        map = googleMapView.createMap(mapOptions);
    }

    @FXML
    public void addressTextFieldAction(ActionEvent event) {
        geocodingService.geocode(address.get(), (GeocodingResult[] results, GeocoderStatus status) -> {

            LatLong latLong = null;

            if( status == GeocoderStatus.ZERO_RESULTS) {
                Alert alert = new Alert(Alert.AlertType.ERROR, "No matching address found");
                alert.show();
                return;
            } else if( results.length > 1 ) {
                Alert alert = new Alert(Alert.AlertType.WARNING, "Multiple results found, showing the first one.");
                alert.show();
                latLong = new LatLong(results[0].getGeometry().getLocation().getLatitude(), results[0].getGeometry().getLocation().getLongitude());
            } else {
                latLong = new LatLong(results[0].getGeometry().getLocation().getLatitude(), results[0].getGeometry().getLocation().getLongitude());
            }

            map.setCenter(latLong);

        });
    }


}
