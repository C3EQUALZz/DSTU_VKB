package programmingLanguagesJava.laboratories.GUI.Config;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.net.URLClassLoader;

class ClassFinder {
    public static Class<?> getaClass(File file) {

        Class<?> result = null;

        try (URLClassLoader classLoader = new URLClassLoader(new URL[]{file.toURI().toURL()})) {

            // Получаем путь файла через точки, которые требует classLoader
            String className = relativePathThroughPoints(file.getAbsolutePath());

            // Загружаем класс
            result = classLoader.loadClass(className);

        } catch (ClassNotFoundException | IOException e) {
            e.printStackTrace();
        }

        return result;
    }

    private static String relativePathThroughPoints(String javaAbsolutePath) {

        int startOfJavaIndex = javaAbsolutePath.indexOf("programmingLanguagesJava");

        return javaAbsolutePath.replace(".java", "")
                .replace("\\", ".")
                .substring(startOfJavaIndex);
    }

}
