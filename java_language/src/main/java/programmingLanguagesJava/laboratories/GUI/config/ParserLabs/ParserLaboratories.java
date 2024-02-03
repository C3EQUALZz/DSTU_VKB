package programmingLanguagesJava.laboratories.GUI.config.ParserLabs;


import java.io.File;
import java.lang.reflect.Method;
import java.util.*;

public class ParserLaboratories {
    public static TreeMap<Class<?>, Method[]> parseLaboratories() {

        String path = System.getProperty("user.dir") + "/src/main/java/programmingLanguagesJava/laboratories";
        var dirWhereAllLaboratories = new File(path);

        var classes = new ArrayList<Class<?>>();

        findClasses(dirWhereAllLaboratories, classes);

        return getInfo(classes);
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
                clazz = ClassFinder.getaClass(file);
                // Добавляем загруженный класс в список
                classes.add(clazz);
            }
        }
    }

    private static TreeMap<Class<?>, Method[]> getInfo(ArrayList<Class<?>> arrayList) {

        var dictionary = new TreeMap<Class<?>, Method[]>(new LaboratoryComparator());

        arrayList.forEach(clazz -> {

            var value = Arrays.stream(clazz.getDeclaredMethods())
                    .filter(method -> method.getName().endsWith("Question"))
                    .sorted(new StringNumberComparator()).toArray(Method[]::new);

            dictionary.put(clazz, value);
        });

        return dictionary;
    }
}
