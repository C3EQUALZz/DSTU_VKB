/**
 * Данный класс является обработчиком событий на тот момент, если оператор решил выбрать здание через карту,
 * а не по поиску, вводя текст в TextField.
 * Документация к тому, чтобы работать с маркером: https://www.sothawo.com/projects/mapjfx-demo/
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.processingEventsOnMap;

import com.sothawo.mapjfx.Coordinate;
import com.sothawo.mapjfx.MapView;
import com.sothawo.mapjfx.Marker;
import com.sothawo.mapjfx.event.MapViewEvent;
import javafx.animation.Transition;
import javafx.scene.control.TextField;
import javafx.util.Duration;

class MapClickController {
    private final MapView mapView;
    private TextField addressField = null;
    private static final Marker markerClick = Marker.createProvided(Marker.Provided.BLUE).setVisible(true);

    MapClickController(MapView mapView) {
        this.mapView = mapView;
    }

    void setAddressField(TextField addressField) {
        this.addressField = addressField;
    }

    void event() {
        mapView.addEventHandler(MapViewEvent.MAP_CLICKED, event -> {
            event.consume();
            final Coordinate newPosition = event.getCoordinate();

            if (addressField != null)
                addressField.setText(ReverseGeocoding.getAddressByCoordinates(newPosition.getLatitude(), newPosition.getLongitude()));

            if (markerClick.getVisible()) {
                final Coordinate oldPosition = markerClick.getPosition();
                if (oldPosition != null) {
                    animateClickMarker(oldPosition, newPosition);
                } else {
                    markerClick.setPosition(newPosition);
                    // adding can only be done after coordinate is set
                    mapView.addMarker(markerClick);
                }
            }
        });
    }


    private static void animateClickMarker(Coordinate oldPosition, Coordinate newPosition) {
        final Transition transition = new Transition() {
            private final Double oldPositionLongitude = oldPosition.getLongitude();
            private final Double oldPositionLatitude = oldPosition.getLatitude();
            private final double deltaLatitude = newPosition.getLatitude() - oldPositionLatitude;
            private final double deltaLongitude = newPosition.getLongitude() - oldPositionLongitude;

            {
                setCycleDuration(Duration.seconds(0.5));
                setOnFinished(evt -> markerClick.setPosition(newPosition));
            }

            @Override
            protected void interpolate(double v) {
                final double latitude = oldPosition.getLatitude() + v * deltaLatitude;
                final double longitude = oldPosition.getLongitude() + v * deltaLongitude;
                markerClick.setPosition(new Coordinate(latitude, longitude));
            }
        };
        transition.play();
    }

}
