/**
 * Данный класс реализует отдельного человека
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Класс Person представляет собой модель человека с полями для имени, фамилии, отчества и должности.
 * Используется для хранения и обработки информации о людях.
 */
@AllArgsConstructor
@Data
public class Person {
    private String secondName;
    private String firstName;
    private String patronymic;
    private int post;

    /**
     * Метод createPeoples() преобразует строку с информацией о людях в список объектов Person.
     *
     * @param allPeople Строка, содержащая информацию о людях. Каждый человек должен быть разделен запятой.
     * @param mainPersonName Имя главного человека. Должность этого человека будет установлена в 1.
     * @return Список объектов Person, представляющих людей.
     */
    public static List<Person> createPeoples(String allPeople, String mainPersonName) {
        return Arrays.stream(allPeople.split(", "))
                .map(human -> {
                    var iterator_human = Arrays.stream(human.split("\\s+")).iterator();

                    var secondName = iterator_human.next();
                    var firstName = iterator_human.next();
                    var patronymic = iterator_human.next();
                    int post = human.equalsIgnoreCase(mainPersonName) ? 1 : 0;

                    return new Person(secondName, firstName, patronymic, post);
                })
                .collect(Collectors.toList());
    }

}
