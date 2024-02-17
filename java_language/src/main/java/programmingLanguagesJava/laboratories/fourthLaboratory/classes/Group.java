package programmingLanguagesJava.laboratories.fourthLaboratory.classes;

import java.util.*;
import java.util.stream.Collectors;

public class Group {

    private final List<Student> students;

    public Group() {
        this.students = new LinkedList<>();
    }

    public Group(Collection<? extends Student> students) {
        this.students = new LinkedList<>();
        students.forEach(this::add);
    }

    public void add(Student el) {
        students.add(el);
    }

    public HashMap<String, Double> parseInfo(ArrayList<Student> students) {
        var dictionary = new HashMap<String, ArrayList<Double>>();
        String[] lessons = {"Математика", "Русский", "Физика", "Информатика", "Литература"};
        Arrays.stream(lessons).forEach(x -> dictionary.put(x, new ArrayList<>()));

        for (var student: students) {
            for (var lesson: lessons) {
                dictionary.get(lesson).add(student.getEvaluations().get(lesson));
            }
        }

        // Считаем средние оценки для каждого предмета
        var averages = new HashMap<String, Double>();
        for (var lesson : lessons) {
            double average = dictionary.get(lesson).stream()
                    .mapToDouble(Double::doubleValue)
                    .average()
                    .orElse(0.0); // Если список пустой, среднее значение будет равно 0
            averages.put(lesson, average);
        }

        return averages;
    }

    public String getAverage() {
        var first = new ArrayList<Student>();
        var second = new ArrayList<Student>();
        for (var student: this.students) {
            if (student.getGroupNumber() == 1) {
                first.add(student);
            }
            else {
                second.add(student);
            }
        }
        return String.format("\n1 группа: %s\n2 группа: %s", parseInfo(first), parseInfo(second));
    }

    public void sort() {
        this.students.sort(Student::compareTo);
    }


    public Student getOldestStudent() {
        return students.stream().max(Comparator.comparingInt(Student::getYearOfBirth)).orElseThrow();
    }

    public Student getYoungestStudent() {
        return students.stream().min(Comparator.comparingInt(Student::getYearOfBirth)).orElseThrow();
    }

    public Student getBest() {
        return students.stream().max(Comparator.comparingDouble(student -> student
                .getEvaluations()
                .values()
                .stream()
                .mapToDouble(Double::doubleValue).average().orElse(0.0))).orElseThrow();
    }

    @Override
    public String toString() {
        return "Группа:\n" + students.stream().map(Student::toString).collect(Collectors.joining("\n"));

    }
}
