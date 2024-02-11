package programmingLanguagesJava.laboratories.GUI.config;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileReader;
import java.io.IOException;

public class JsonSimpleParser {

    private static final JSONParser parser = new JSONParser();
    private final JSONObject jsonObject;

    public JsonSimpleParser() {
        this.jsonObject = parse();
    }

    private static JSONObject parse() {

        try (FileReader fileReader = new FileReader("src/main/resources/laboratoriesFiles/condition.json")) {

            return (JSONObject) parser.parse(fileReader);

        } catch (IOException | ParseException e) {
            return null;
        }
    }

    public String get(String laboratoryNumber, String task) {
        var lab = (JSONObject) jsonObject.get(laboratoryNumber);
        return (String) lab.get(task);
    }

}
