package programmingLanguagesJava.laboratories.GUI.Config;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;

public class Parser {
    public static void main(String[] args) throws MalformedURLException, ClassNotFoundException {

        var classes = new ArrayList<Class<?>>();
        var dir = new File("java_language/src/main/java/programmingLanguagesJava/laboratories");
        findClasses(dir, classes);

        System.out.println(classes);
    }

    private static void findClasses(File directory, ArrayList<Class<?>> classes) {

        var files = directory.listFiles();

        if (files == null)
            return;

        for (var file : files) {

            if (file.isDirectory())
                findClasses(file, classes);

            else if (file.getName().startsWith("Solution")) {
                // Получаем абсолютный путь к файлу
                Class<?> clazz;
                try {
                    clazz = getaClass(file);
                } catch (MalformedURLException | ClassNotFoundException e) {
                    throw new RuntimeException(e);
                }
                // Добавляем загруженный класс в список
                classes.add(clazz);
            }
        }
    }

    private static Class<?> getaClass(File file) throws MalformedURLException, ClassNotFoundException {
        // Преобразуем абсолютный путь в URL
        URL url = file.toURI().toURL();
        // Создаем URLClassLoader с одним элементом - URL к файлу класса
        URLClassLoader classLoader = new URLClassLoader(new URL[]{url});
        // Загружаем класс
        return classLoader.loadClass(file.getName().substring(0, file.getName().length() - 5));
    }

}
