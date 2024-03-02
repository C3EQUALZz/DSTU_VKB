/**
 * Здесь происходит обработка запросов с помощью сервиса:
 * mapjfx возвращает только координаты, а для оператора нужно распознавание объекта (страна, улица, город, ...)
 * Мы же в Google картах не вбиваем координаты, а только название. Здесь реализован именно функционал.
 */
package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

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

    // Метод, с помощью которого происходит взаимодействие (интерфейс образный).
    // Здесь мы передаем широту и долготу, чтобы получить имя.
    static String getAddressByCoordinates(double latitude, double longitude) {
        // Здесь мы получаем JSON информацию с сервера
        var connection = makeRequest(latitude, longitude);
        // Здесь мы собираем полностью информацию с JSON
        var stringBuilderData = collectInfo(connection);

        return getDisplayName(stringBuilderData);
    }

    // Создание запроса по широте и долготе с помощью API.
    private static HttpURLConnection makeRequest(double latitude, double longitude) {
        HttpURLConnection connection;

        try {
            // Безопасный запрос к API делается через URI. Конструктор URL - небезопасный.
            var uri = new URI(String.format("%s?format=json&lat=%f&lon=%f", NOMINATIM_API_URL, latitude, longitude));
            var url = uri.toURL();
            // Сделали подключение, теперь отправляем запрос "GET" на сервер, чтобы собрать информацию.
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.connect();

        } catch (Exception e) {
            throw new RuntimeException("Нет подключения к серверу\n" + e);
        }

        return connection;
    }

    // Сбор информации в строку, чтобы можно было десериализовать JSON
    private static StringBuilder collectInfo(HttpURLConnection connection) {
        String line;
        var result = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {

            while ((line = reader.readLine()) != null)
                result.append(line);

        } catch (IOException e) {
            throw new RuntimeException("Не получилось собрать json информацию по карте\n" + e);
        }

        return result;
    }

    // Получаем информацию о месте
    private static String getDisplayName(StringBuilder stringBuilder) {
        String display_name;

        try {

            JSONObject jsonObject = (JSONObject) jsonParser.parse(stringBuilder.toString());
            display_name = (String) jsonObject.get("display_name");

        } catch (ParseException e) {
            throw new RuntimeException("Не получилось распарсить json файл\n" + e);
        }

        return display_name;
    }
}
