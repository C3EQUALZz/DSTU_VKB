package programmingLanguagesJava.laboratories.GUI.Config;

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.io.File;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.text.ParseException;
import java.util.*;

public class Parser {
    public static void main(String[] args) throws MalformedURLException, ClassNotFoundException {

        var dirWhereAllLaboratories = new File("java_language/src/main/java/programmingLanguagesJava/laboratories");

        var classes = new ArrayList<Class<?>>();

        findClasses(dirWhereAllLaboratories, classes);

        uwu(classes);
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
                clazz = ClassFinder.getaClass(file);
                // Добавляем загруженный класс в список
                classes.add(clazz);
            }
        }
    }

    private static void uwu(ArrayList<Class<?>> arrayList) {
        Class<?> clazz = arrayList.getFirst();
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            if (method.getName().endsWith("Question"))
                System.out.println(method.getName());
        }

        List<String> list = Arrays.asList("third", "first", "second");
        list.sort(new Comparator<>() {
            @Override
            public int compare(String o1, String o2) {
                return Integer.compare(numberFromString(o1), numberFromString(o2));
            }

            private int numberFromString(String number) {

                RuleBasedNumberFormat numberFormat = new RuleBasedNumberFormat(Locale.UK, RuleBasedNumberFormat.SPELLOUT);
                try {
                    return numberFormat.parse(number).intValue();
                } catch (ParseException e) {
                    return -1;
                }
            }
        });
        System.out.println(list);
    }
}
