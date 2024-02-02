package programmingLanguagesJava.laboratories.GUI.Config;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Modifier;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Objects;
import java.util.stream.Stream;

public class Parser {
    public static void main(String[] args) throws MalformedURLException, ClassNotFoundException {

        var classes = new ArrayList<Class<?>>();
        var dir = new File("java_language/src/main/java/programmingLanguagesJava/laboratories");
        findClasses(dir, classes);

        System.out.println(classes);
    }

    private static void findClasses(File directory, ArrayList<Class<?>> classes) throws ClassNotFoundException {

        Arrays.stream(Objects.requireNonNull(directory.listFiles())).filter(File::isDirectory);
    }

}
