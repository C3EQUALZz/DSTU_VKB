package programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import lombok.Getter;

/**
 * Класс, чтобы считывать информацию из файла, которая нужна для обнаружения.
 * Он не каждый раз запускается для считывания, можно было один раз по идее ввод открывать,
 * но я хочу уже быстрее сдать проект
 */
@Getter
class FileReaderService {

    private final String FILE_PATH = System.getProperty("user.dir") + "/src/main/resources/projectFiles/fileWatch.txt";

    /**
     * Метод, который считывает информацию построчно из файла. Каждый раз читает одну строку
     * @return возвращает информацию с одной строки.
     */
    String readWordFromFile() {

        try (var reader = new BufferedReader(new FileReader(FILE_PATH))) {
            return reader.readLine();
        } catch (IOException e) {
            throw new RuntimeException("Не получилось считать файл", e);
        }

    }

}
