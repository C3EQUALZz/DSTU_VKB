/**
 * Данный файл описывает взаимодействие с TextField для поиска информации. Попытался сделать аналогичный поиск, как в Google.
 * Единственная проблема, что работает не совсем идеально из-за сервиса. Возможен вылет просто по приколу, поэтому надо быть аккуратным.
 * Тут есть дублирование логики с другим классом, где есть запросы к API, но мне исправлять это не особо хочется сейчас.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.searchEngineField;

import com.sothawo.mapjfx.Coordinate;
import com.sothawo.mapjfx.MapView;
import com.sothawo.mapjfx.Marker;
import javafx.scene.control.TextField;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.ElementAddressFillingForm;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class TextFieldSearchController implements ElementAddressFillingForm {
    private MapView mapView;
    private final TextField textField;
    private final JSONParser parser = new JSONParser();
    private static final Marker markerClick = Marker.createProvided(Marker.Provided.BLUE).setVisible(true);

    @SuppressWarnings("unused")
    public TextFieldSearchController(TextField textField) {
        this.textField = textField;
    }

    @SuppressWarnings("unused")
    public void setMapView(MapView mapView) {
        this.mapView = mapView;
    }

    /**
     * Обработчик событий, чтобы запускать логику методов.
     */
    public void event() {

        var connection = connect(textField.getText());

        var data = parseJson(readInfo(connection));

        if (data.equals("Не удалось найти адрес.")) {
            textField.setText("Не удалось найти адрес. Проверьте корректность");

        } else {

            var iteratorData = Arrays.stream(data.split("\\s+")).map(Double::parseDouble).iterator();
            var coords = new Coordinate(iteratorData.next(), iteratorData.next());

            markerClick.setPosition(coords);
            mapView.addMarker(markerClick);
            mapView.setCenter(coords);
        }

        connection.disconnect();

    }

    /**
     * Здесь происходит подключение к серверу, чтобы собрать информацию.
     * @param address адрес, который ввел пользователь в TextField
     * @return возвращает удачное подключение к серверу.
     */
    private HttpURLConnection connect(String address) {

        var NOMINATIM_API = "https://nominatim.openstreetmap.org/search?format=json&q=";
        var encodedAddress = java.net.URLEncoder.encode(address, StandardCharsets.UTF_8);
        var url = NOMINATIM_API + encodedAddress;

        try {

            var uri = new URI(url);
            return (HttpURLConnection) uri.toURL().openConnection();

        } catch (IOException | URISyntaxException e) {

            throw new RuntimeException("Невозможно обработать запрос к API", e);

        }

    }

    /**
     * Обрабатываем информацию, считываем данные
     * @param connection подключение к серверу
     * @return возвращает информацию с сервера в виде строки.
     */
    private StringBuilder readInfo(HttpURLConnection connection) {
        var response = new StringBuilder();

        // Буферно считываю информацию
        try (var in = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {

            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            return response;

        } catch (IOException e) {

            throw new RuntimeException("Невозможно считать JSON файл с сервера", e);

        }

    }

    /**
     * Здесь происходит парсинг JSON, чтобы получить информацию
     * @param jsonData json в виде строки, который мы хотим обработать
     * @return возвращает строку, где (широта, долгота), а в ином случае возвращает ошибку.
     */
    private String parseJson(StringBuilder jsonData) {

        try {
            var jsonArray = (JSONArray) parser.parse(jsonData.toString());

            if (!jsonArray.isEmpty()) {
                var jsonObject = (JSONObject) jsonArray.getFirst();
                return String.format("%s %s", jsonObject.get("lat"), jsonObject.get("lon"));
            }

            return "Не удалось найти адрес.";

        } catch (ParseException e) {

            throw new RuntimeException("Невозможно обработать JSON файл", e);

        }

    }

}
