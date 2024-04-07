package programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import lombok.Getter;

@Getter
class FileReaderService {

    private final String FILE_PATH = System.getProperty("user.dir") + "/src/main/resources/projectFiles/fileWatch.txt";

    public String readWordFromFile() {

        try (var reader = new BufferedReader(new FileReader(FILE_PATH))) {
            return reader.readLine();
        } catch (IOException e) {
            throw new RuntimeException("Не получилось считать файл", e);
        }

    }

}
