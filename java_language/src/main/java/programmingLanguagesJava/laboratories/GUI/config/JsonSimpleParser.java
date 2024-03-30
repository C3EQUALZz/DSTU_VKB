/**
 * В json файле описаны условия для лабораторных работ, поэтому нужно было написать соотв. парсер.
 * Можно было сделать бд, да, но я SQL не знаю совершенно, чтобы такие вещи творить.
 */

package programmingLanguagesJava.laboratories.GUI.config;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileReader;
import java.io.IOException;

public class JsonSimpleParser {

    private static final JSONParser parser = new JSONParser();
    private final JSONObject jsonObject;

    private static JsonSimpleParser instance;

    private JsonSimpleParser() {
        this.jsonObject = parse();
    }

    public static JsonSimpleParser getInstance() {
        if (instance == null) {
            instance = new JsonSimpleParser();
        }
        return instance;
    }

    private static JSONObject parse() {

        // В Java нет контекстного менеджера (по названию), но аналогичная технология называется "try with resources".
        // Так вот, здесь тоже открывается файл на чтение, а потом в конце безопасно закрывается в блоке finally.
        try (FileReader fileReader = new FileReader("src/main/resources/laboratoriesFiles/condition.json")) {

            return (JSONObject) parser.parse(fileReader);

        } catch (IOException | ParseException e) {
            throw new RuntimeException("Не получилось распарсить файл", e);
        }
    }

    /**
     * Обратите внимание на структуру JSON файла, в котором описаны условия для лабораторных работ.
     * @param laboratoryNumber первый ключ, с помощью которого мы получим словарь с заданиями.
     * @param task последний ключ, с помощью которого мы получаем условие задания.
     * @return строку с условием, где описаны все действия.
     */
    public String get(String laboratoryNumber, String task) {
        var lab = (JSONObject) jsonObject.get(laboratoryNumber);
        return (String) lab.get(task);
    }

}
