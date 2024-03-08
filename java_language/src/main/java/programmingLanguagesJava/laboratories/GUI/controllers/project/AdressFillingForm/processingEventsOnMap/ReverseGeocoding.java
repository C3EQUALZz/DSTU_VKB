/**
 * Здесь происходит обработка запросов с помощью сервиса: nominatim.openstreetmap
 * mapjfx возвращает только координаты, а для оператора нужно распознавание объекта (страна, улица, город, ...)
 * Мы же в Google картах не вбиваем координаты, а только название. Здесь реализован именно функционал.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.processingEventsOnMap;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;

class ReverseGeocoding {
    private static final String NOMINATIM_API_URL = "https://nominatim.openstreetmap.org/reverse";
    private static final JSONParser jsonParser = new JSONParser();

    /**
     * Метод, с помощью которого происходит взаимодействие (интерфейс образный).
     * Здесь мы передаем широту и долготу, чтобы получить имя.
     * @param latitude координаты по широте
     * @param longitude координаты по долготе
     * @return возвращает строку с подробным описанием здания.
     */
    static String getAddressByCoordinates(double latitude, double longitude) {
        HttpURLConnection connection = null;

        try {

            connection = makeRequest(latitude, longitude);
            String jsonData = collectInfo(connection);
            return getDisplayName(jsonData);

        } catch (IOException e) {

            throw new RuntimeException("Ошибка при подключении к адресу: " + e.getMessage(), e);

        } finally {

            if (connection != null) {
                connection.disconnect();
            }
        }

    }

    /**
     * Здесь мы соединяемся с сервером, чтобы получить JSON файл, который описывает адрес по широте и долготе
     * @param latitude координаты по широте
     * @param longitude координаты по долготе
     * @return возвращает подключение, с помощью которого
     */
    private static HttpURLConnection makeRequest(double latitude, double longitude) throws IOException {
        try {

            var uri = new URI(String.format("%s?format=json&lat=%f&lon=%f", NOMINATIM_API_URL, latitude, longitude));
            var url = uri.toURL();
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.connect();
            return connection;

        } catch (Exception e) {

            throw new IOException("Невозможно подключиться к серверу", e);

        }
    }

    // Сбор информации в строку, чтобы можно было десериализовать JSON
    private static String collectInfo(HttpURLConnection connection) {
        var result = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {

            var line = "";

            while ((line = reader.readLine()) != null) {
                result.append(line);
            }

            return result.toString();

        } catch (IOException e) {

            throw new RuntimeException("Не удалось считать JSON данные", e);

        }
    }

    // Получаем информацию о месте
    private static String getDisplayName(String jsonData) {

        try {

            var jsonObject = (JSONObject) jsonParser.parse(jsonData);
            return (String) jsonObject.get("display_name");

        } catch (ParseException e) {

            throw new RuntimeException("Не удалось распарсить данные", e);

        }

    }
}
