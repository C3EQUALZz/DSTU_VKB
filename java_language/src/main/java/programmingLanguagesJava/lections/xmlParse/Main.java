/**
 * Точка запуска программы, где мы хотим прочитать наш XML файл
 */

package programmingLanguagesJava.lections.xmlParse;

import programmingLanguagesJava.lections.xmlParse.DAO.Student;
import programmingLanguagesJava.lections.xmlParse.fileInteraction.Parser;
import programmingLanguagesJava.lections.xmlParse.fileInteraction.XMLParser;

import java.io.File;

public class Main {
    public static void main(String[] args) {
        Parser parser = new XMLParser();
        var students = parser.parse(new File("java_language/src/main/java/programmingLanguagesJava/lections/xmlParse/student.xml"));

        for (Student student : students.getStudent()) {
            System.out.println("Имя: " + student.getName());
            System.out.println("Возраст: " + student.getAge());
            System.out.println("Специальность: " + student.getMajor());
            System.out.println("--------------------");
        }
    }
}
