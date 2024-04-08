/**
 * Данный класс является настройкой для combobox, здесь я выставляю конфигурационные параметры.
 * Там удобная настройка звуков, анимаций и т.п. Сделано с той целью, чтобы избежать дублирования кода
 * Не нарушать модульность программы.
 */

package programmingLanguagesJava.laboratories.GUI.config;

import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ListCell;
import programmingLanguagesJava.laboratories.GUI.config.ParserLabs.ParserLaboratories;

import java.lang.reflect.Method;
import java.util.Collection;
import java.util.LinkedList;
import java.util.TreeMap;
import java.util.stream.IntStream;

public class ComboboxConfigurator {
    // Словарь с лабораторными работами, где ключ - лабораторная работа, значение - ссылки на методы
    private final TreeMap<Class<?>, Method[]> dictInfoLaboratories = ParserLaboratories.parseLaboratories();
    private static ComboboxConfigurator instance;

    private ComboboxConfigurator() {}

    public static ComboboxConfigurator getInstance() {
        if (instance == null) {
            instance = new ComboboxConfigurator();
        }
        return instance;
    }

    /**
     * Конфигурация выпадающего списка по умолчанию. Тут только установка звуков.
     * @param comboBox выпадающий список, который мы хотим настроить.
     */
    public void defaultConfiguration(ComboBox<String> comboBox) {

        // Обработчик событий, когда мышка попала на combobox.
        comboBox.setOnMouseEntered(event -> SOUND.HOVER.play());

        // Обработчик событий, когда нажали на combobox.
        comboBox.setOnMouseClicked(event -> SOUND.CLICK.play());

        // Это было ради того, чтобы установить эффект hover звука на каждый элемент в combobox.
        comboBox.setCellFactory(param -> new ListCell<>() {
            @Override
            protected void updateItem(String item, boolean empty) {
                super.updateItem(item, empty);
                if (empty || item == null) {
                    setText(null);
                } else {
                    setText(item);
                    setOnMouseEntered(event1 -> SOUND.HOVER.play());
                }
            }
        });

        // Самое интересное, что установить звук нажатия через setCellFactory не работало. Под капотом идеально
        // устройство не разбирал, поэтому такой вариант для обработки звука.
        comboBox.getSelectionModel().selectedItemProperty().addListener((observable, oldValue, newValue) -> {
            if (newValue != null) {
                SOUND.CLICK.play();
            }
        });

        // Отключаю с той целью, когда пользователь ещё не выбрал лабораторные
        comboBox.setDisable(true);
    }

    /**
     * В лабораторных работах я настраиваю combobox, поэтому вот здесь решил оставить настройку.
     * У меня в зависимости от кнопки выбираются и обновляются значения в combobox
     * @param comboBox выпадающий список, который мы хотим настроить
     * @param button кнопка, относительно которой будет настройка по заданиям
     */
    public void setupComboboxEvent(ComboBox<String> comboBox, Button button) {

        // Сохранение выбранного значения, если оно есть
        var selectedValue = comboBox.getValue();

        // Перед тем как добавлять элементы, я удаляю все оттуда. Высчитывать разницу и вот эти все приколы не хочу
        comboBox.getItems().clear();

        // Получаю из словаря с лабораторными работами количество заданий
        var countOfMethods = dictInfoLaboratories.get(getKeyButton(button)).length;

        // O(1) - сложность добавления в связный список, поэтому сделал его. Добавляю туда соотв количество заданий
        var linkedList = new LinkedList<String>();
        IntStream.range(1, countOfMethods + 1).forEach(number -> linkedList.add(number + " задание"));

        comboBox.getItems().addAll(linkedList);

        if (selectedValue != null) {

            if (comboBox.getItems().contains(selectedValue))
                comboBox.setValue(selectedValue);

            else
                comboBox.getSelectionModel().selectFirst();

        }
    }

    public void setupComboboxEvent(ComboBox<String> comboBox, Collection<String> nameOfPersons) {
        comboBox.setDisable(false);

        // Сохранение выбранного значения, если оно есть
        var selectedValue = comboBox.getValue();

        comboBox.getItems().clear();

        comboBox.getItems().addAll(nameOfPersons);

        if (selectedValue != null) {

            if (comboBox.getItems().contains(selectedValue))
                comboBox.setValue(selectedValue);

            else
                comboBox.getSelectionModel().selectFirst();

        }
    }

    /**
     * Для чего нужен данный метод? Вся проблема в том, что у меня словарь содержит ссылки на классы. В зависимости от текста
     * кнопки я придумал такой костыль, который помогает найти ссылку на класс.
     * Например, нажали на кнопку "0 лабораторная" -> индекс лабораторной (0) -> массив лабораторных[0] ->
     * ссылка на 0 лабораторную из словаря -> получаю информацию о данном классе (кол-во методов, ссылки на них и т.п).
     * @param button кнопка, на которую нажал пользователь.
     * @return ссылку на класс с лабораторной работой.
     */
    public Class<?> getKeyButton(Button button) {
        // Получаем текст с кнопки ("0 лабораторная") -> ["0", "лабораторная"] -> "0" -> 0 -> zeroLaboratory.Solution
        int index = numerator(button.getText().split(" ")[0]);
        return (Class<?>) dictInfoLaboratories.keySet().toArray()[index];
    }

    public Class<?> getKeyButton(String text) {
        int index = numerator(text.split(" ")[0]);
        return (Class<?>) dictInfoLaboratories.keySet().toArray()[index];
    }

    /**
     * Вспомогательный метод, который нужен для обработки лабораторных работ.
     * Можно было сделать словарь, да, быстрее, но тут небольшой выйгрыш.
     * @param numberOfLaboratory номер лабораторной работы
     * @return индекс нашей лабораторной работы, который я буду искать в массиве.
     */
    private int numerator(String numberOfLaboratory) {
        return switch (numberOfLaboratory) {
            case "0" -> 0;
            case "1" -> 1;
            case "1.1" -> 2;
            case "2" -> 3;
            case "3" -> 4;
            case "3.1" -> 5;
            case "4" -> 6;
            default -> Integer.MAX_VALUE;
        };
    }

}
