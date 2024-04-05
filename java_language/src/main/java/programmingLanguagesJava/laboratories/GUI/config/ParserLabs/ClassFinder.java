package programmingLanguagesJava.laboratories.GUI.config.ParserLabs;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.net.URLClassLoader;

/**
 * Класс ClassFinder используется для загрузки классов из файлов .java.
 */
class ClassFinder {
    /**
     * Метод getaClass принимает файл .java и возвращает соответствующий класс.
     *
     * @param file Файл .java, который нужно загрузить.
     * @return Загруженный класс.
     * @throws RuntimeException Если класс не удалось загрузить.
     */
    static Class<?> getaClass(File file) {

        Class<?> result;

        try (var classLoader = new URLClassLoader(new URL[]{file.toURI().toURL()})) {

            // Получаем путь файла через точки, которые требует classLoader
            var className = relativePathThroughPoints(file.getAbsolutePath());

            // Загружаем класс
            result = classLoader.loadClass(className);

        } catch (ClassNotFoundException | IOException e) {
            throw new RuntimeException("Не получилось загрузить класс " + file.getAbsolutePath(), e);
        }

        return result;
    }

    /**
     * Метод relativePathThroughPoints преобразует абсолютный путь файла в относительный путь с точками.
     *
     * @param javaAbsolutePath Абсолютный путь к файлу .java.
     * @return Относительный путь с точками.
     */
    private static String relativePathThroughPoints(String javaAbsolutePath) {

        var startOfJavaIndex = javaAbsolutePath.indexOf("programmingLanguagesJava");

        return javaAbsolutePath.replace(".java", "")
                .replace("\\", ".")
                .substring(startOfJavaIndex);
    }

}
