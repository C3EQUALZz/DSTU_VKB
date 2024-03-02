/**
 * Данный класс описывает взаимодействие с картой, здесь у нас происходят все взаимодействия с картой.
 * Здесь есть логика нажатия на карту, установка маркеров
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import com.sothawo.mapjfx.Coordinate;
import com.sothawo.mapjfx.MapView;
import com.sothawo.mapjfx.Marker;
import com.sothawo.mapjfx.event.MapViewEvent;
import javafx.animation.Transition;
import javafx.scene.control.TextField;
import javafx.util.Duration;

class OpenStreetMap {
    private final MapView mapView;
    private final Marker markerClick = Marker.createProvided(Marker.Provided.BLUE).setVisible(true);
    private final TextField addressField;

    OpenStreetMap(MapView mapView, TextField addressField) {
        this.mapView = mapView;
        this.addressField = addressField;
    }

    // Главный event, который описывает действия с картой
    void mapViewEvent() {
        // Создание карты
        mapView.initialize();
        // Установка начальных координат на ДГТУ
        mapView.setCenter(new Coordinate(47.2371576587879, 39.711658338598745));
        // Приближение карты по умолчанию. Выбрал на глаз.
        mapView.setZoom(17);
        // Event, который отвечает за установку маркера на карту.
        markerEvent();


    }

    // Данный код был полностью взят отсюда: https://www.sothawo.com/projects/mapjfx-demo/
    private void markerEvent() {
        mapView.addEventHandler(MapViewEvent.MAP_CLICKED, event -> {
            event.consume();
            final Coordinate newPosition = event.getCoordinate();
            addressField.setText(String.valueOf(newPosition));

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

    // Данный код был взят отсюда: https://www.sothawo.com/projects/mapjfx-demo/
    private void animateClickMarker(Coordinate oldPosition, Coordinate newPosition) {
        // animate the marker to the new position
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
