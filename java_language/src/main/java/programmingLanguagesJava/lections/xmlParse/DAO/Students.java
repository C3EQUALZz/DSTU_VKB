/**
 * Класс выполняет принцип DAO, описывая всех студентов
 */

package programmingLanguagesJava.lections.xmlParse.DAO;

import javax.xml.bind.annotation.XmlRootElement;
import java.util.List;
import lombok.Setter;
import lombok.Getter;

/**
 * Класс, который описывает всех студентов.
 */
@Getter
@Setter
@XmlRootElement(name = "students")
public class Students {
    private List<Student> student;
}
