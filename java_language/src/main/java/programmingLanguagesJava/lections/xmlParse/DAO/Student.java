/**
 * Класс, который описывает одного студента. Здесь также используется принцип DAO
 */

package programmingLanguagesJava.lections.xmlParse.DAO;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Student {
    private String name;
    private int age;
    private String major;
}