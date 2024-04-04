/**
 * Данный класс больше направлен на дальнейшую обработку файлов.
 * Новые методы пока не придуманы, но можно здесь делать
 */
package programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * Класс FileUtil содержит утилиты для работы с файлами.
 */
public class FileUtil {

    /**
     * Читает все байты из файла по указанному пути.
     *
     * @param filePath Путь к файлу, который нужно прочитать. Это должен быть абсолютный путь.
     * @return Массив байтов, содержащий данные из файла.
     * @throws RuntimeException Если произошла ошибка при чтении файла или файл не найден.
     */
    public static byte[] readBytesFromFile(String filePath) {

        try {

            return Files.readAllBytes(Paths.get(filePath));

        } catch (IOException | NullPointerException e) {

            throw new RuntimeException("Ошибка при чтении файла, а возможно и не найден " + filePath, e);

        }

    }
}
