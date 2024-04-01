package programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils;

import lombok.Data;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Data
public class Person {
    private String secondName;
    private String firstName;
    private String patronymic;
    private int post;

    public static List<Person> createPeoples(String allPeople, String mainPersonName) {
        List<Person> people = new ArrayList<>();

        for (var human : allPeople.split(", ")) {

            var iterator_human = Arrays.stream(human.split("\\s+")).iterator();

            String secondName = iterator_human.next();
            String firstName = iterator_human.next();
            String patronymic = iterator_human.next();
            int post = human.equalsIgnoreCase(mainPersonName) ? 1 : 0;

            Person person = new Person();
            person.setSecondName(secondName);
            person.setFirstName(firstName);
            person.setPatronymic(patronymic);
            person.setPost(post);

            people.add(person);
        }

        return people;
    }

}
