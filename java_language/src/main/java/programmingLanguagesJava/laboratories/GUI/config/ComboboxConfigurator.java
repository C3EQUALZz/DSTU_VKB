package programmingLanguagesJava.laboratories.GUI.config;

import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ListCell;
import programmingLanguagesJava.laboratories.GUI.config.ParserLabs.ParserLaboratories;

import java.lang.reflect.Method;
import java.util.LinkedList;
import java.util.TreeMap;
import java.util.stream.IntStream;

public class ComboboxConfigurator {
    private final ButtonConfigurator buttonConfigurator = new ButtonConfigurator();
    private final TreeMap<Class<?>, Method[]> dictInfoLaboratories = ParserLaboratories.parseLaboratories();

    public void defaultConfiguration(ComboBox<String> comboBox) {

        comboBox.setOnMouseEntered(event -> buttonConfigurator.hoverClip.play());

        comboBox.setOnMouseClicked(event -> buttonConfigurator.clickClip.play());

        comboBox.setCellFactory(param -> new ListCell<>() {
            @Override
            protected void updateItem(String item, boolean empty) {
                super.updateItem(item, empty);
                if (empty || item == null) {
                    setText(null);
                } else {
                    setText(item);
                    setOnMouseEntered(event1 -> buttonConfigurator.hoverClip.play());
                }
            }
        });

        comboBox.getSelectionModel().selectedItemProperty().addListener((observable, oldValue, newValue) -> {
            if (newValue != null) {
                buttonConfigurator.clickClip.play();
            }
        });

        comboBox.setDisable(true);
    }

    public void setupComboboxEvent(ComboBox<String> comboBox, Button button) {
        comboBox.setDisable(false);

        // Сохранение выбранного значения, если оно есть
        var selectedValue = comboBox.getValue();

        comboBox.getItems().clear();

        var countOfMethods = dictInfoLaboratories.get(getKeyButton(button)).length;

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

    private Class<?> getKeyButton(Button button) {
        int index = numerator(button.getText().split(" ")[0]);
        return (Class<?>) dictInfoLaboratories.keySet().toArray()[index];
    }

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
