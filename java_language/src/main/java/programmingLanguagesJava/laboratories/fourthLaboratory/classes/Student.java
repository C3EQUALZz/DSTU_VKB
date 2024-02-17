package programmingLanguagesJava.laboratories.fourthLaboratory.classes;

import com.github.javafaker.Faker;
import org.jetbrains.annotations.NotNull;

import java.util.HashMap;
import java.util.Random;

public class Student implements Comparable<Student> {
    private final String FIO;
    private final int course;
    private final int yearOfBirth;
    private final int groupNumber;
    private HashMap<String, Double> evaluations;

    public Student() {
        this.FIO = new Faker().name().name();
        this.yearOfBirth = 2024 - new Random().nextInt(18, 28);
        this.groupNumber = new Random().nextInt(1, 3);
        this.course = new Random().nextInt(1, 6);
        this.evaluations = initMap();
    }

    @Override
    public String toString() {

        return String.format("Студент %s, курс %d, %d года рождения, номер группы %d, оценки %s",
                FIO, course, yearOfBirth, groupNumber, evaluations);
    }

    public int getYearOfBirth() {
        return yearOfBirth;
    }

    public int getGroupNumber() {
        return groupNumber;
    }

    public HashMap<String, Double> getEvaluations() {
        return evaluations;
    }

    @Override
    public int compareTo(@NotNull Student otherStudent) {
        // Сначала сравниваем по курсу
        if (this.course != otherStudent.course)
            return Integer.compare(this.course, otherStudent.course);
        // Если курсы одинаковы, сравниваем по фамилии
        return this.FIO.compareTo(otherStudent.FIO);
    }

    private HashMap<String, Double> initMap() {
        var result = new HashMap<String, Double>();
        String[] lessons = {"Математика", "Русский", "Физика", "Информатика", "Литература"};

        for (var lesson : lessons) {
            result.put(lesson, Double.parseDouble(String.format("%.2f", new Random().nextDouble(2.0, 5.0))));
        }

        return result;
    }
}
