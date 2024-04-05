package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategy;

import javafx.scene.control.TextArea;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.config.JsonSimpleParser;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext.StrategyContextCombobox;

import java.util.Optional;

/**
 * Класс, который добавляет взаимодействие для ComboBox. Тут некоторая предварительная настройка для выпадающего списка.
 */
@RequiredArgsConstructor
public class ComboboxActionLaboratories implements ActionLaboratories {

    private final StrategyContextCombobox strategyContextCombobox;
    private final TextArea condition;
    private final JsonSimpleParser data = JsonSimpleParser.getInstance();

    /**
     * Здесь именно запускается настройка.
     */
    @Override
    public void execute() {
        var combobox = strategyContextCombobox.getCombobox();
        var buttonClickListener = strategyContextCombobox.getButtonClickListener();

        comboboxConfigurator.defaultConfiguration(combobox);

        combobox.valueProperty().addListener((obs, oldVal, newVal) ->
                Optional.ofNullable(newVal).ifPresent(value -> {

                    var lastClickedButton = Optional.ofNullable(buttonClickListener.getLastClickedButton());

                    lastClickedButton.ifPresent(button -> {
                        var buttonText = button.getText();
                        var text = data.get(buttonText, value);
                        condition.setText(text);
                    });
                }));
    }
}
