/**
 * Данный класс отвечает за добавление элементов в combobox.
 * Здесь все элементы уникальный, порядка нет при сохранении.
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.addingNames;

import javafx.scene.control.TextField;
import programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.ElementAddressFillingForm;

import java.util.HashSet;

public class TextFieldAddController implements ElementAddressFillingForm {

    private final TextField textField;

    private final HashSet<String> persons = new HashSet<>();

    public TextFieldAddController(TextField textField) {
        this.textField = textField;
    }

    /**
     * Здесь запускается обработчик событий, который у нас добавляет элементы в множество
     */
    @Override
    public void event() {
        persons.add(textField.getText());
        textField.clear();
    }

    /**
     * Геттер, который возвращает нам информацию о людях в множестве
     * @return множество с людьми
     */
    public HashSet<String> getPersons() {
        return this.persons;
    }

}
