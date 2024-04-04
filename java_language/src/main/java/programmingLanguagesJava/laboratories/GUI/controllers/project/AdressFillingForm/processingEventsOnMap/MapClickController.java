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
import javafx.concurrent.Task;
import javafx.scene.control.TextField;
import javafx.util.Duration;
import org.jetbrains.annotations.NotNull;
import lombok.Setter;

import java.util.Optional;

class MapClickController {
    // Карта, к которой мы хотим применить наш контроллер
    private final MapView mapView;
    // TextField, к которому мы обращаемся для заполнения.
    @Setter
    private TextField addressField = null;
    // Именно сам маркер
    private final Marker markerClick = Marker.createProvided(Marker.Provided.BLUE).setVisible(true);

    MapClickController(MapView mapView) {
        this.mapView = mapView;
    }

    /**
     * Event, который предназначен для обработки нажатий на карту.
     */
    void event() {
        mapView.addEventHandler(MapViewEvent.MAP_CLICKED, event -> {
            event.consume();
            final Coordinate newPosition = event.getCoordinate();
            final Coordinate oldPosition = markerClick.getPosition();

            // Создаем новую задачу для выполнения запроса к API в отдельном потоке.
            // Запускаем задачу в новом потоке
            new Thread(setNameByCoords(newPosition)).start();

            if (oldPosition != null) {
                animateClickMarker(oldPosition, newPosition);
            } else {
                markerClick.setPosition(newPosition);
                mapView.addMarker(markerClick);
            }
        });
    }

    /**
     * Запросы к API нужно оформлять в отдельном потоке, поэтому здесь создал отдельный метод, который делает запрос
     * @param newPosition координаты, которые выбрал пользователь для обработки
     * @return задачу, где находится элемент строки для вставки в текст
     */
    @NotNull
    private Task<String> setNameByCoords(Coordinate newPosition) {
        var task = new Task<String>() {
            @Override
            protected String call() {
                return ReverseGeocoding.getAddressByCoordinates(newPosition.getLatitude(), newPosition.getLongitude());
            }
        };

        // Обновляем поле адреса после завершения задачи
        task.setOnSucceeded(workerStateEvent -> {
            String address = task.getValue();
            Optional.ofNullable(addressField).ifPresent(field -> field.setText(address));
        });

        return task;
    }


    /**
     * Анимация передвижения маркера, была взята с документации к карте
     * @param oldPosition старая позиция по координатам
     * @param newPosition новая позиция по координатам
     */
    private void animateClickMarker(Coordinate oldPosition, Coordinate newPosition) {
        final Transition transition = new Transition() {
            private final double deltaLatitude = newPosition.getLatitude() - oldPosition.getLatitude();
            private final double deltaLongitude = newPosition.getLongitude() - oldPosition.getLongitude();

            {
                setCycleDuration(Duration.seconds(0.5));
                setOnFinished(evt -> markerClick.setPosition(newPosition));
            }
            // Данная формула была в документации, честно не разбирался что и как
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
