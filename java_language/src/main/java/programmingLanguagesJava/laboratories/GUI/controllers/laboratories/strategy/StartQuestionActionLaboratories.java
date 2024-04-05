package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategy;

import javafx.scene.control.Button;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.ConsoleReader;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext.StrategyContextCombobox;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext.StrategyContextText;

/**
 * Класс, который является логикой запуска решения задания.
 * Здесь как раз считываются все аргументы, которые выбрал пользователь, а потом вставляется текст с результатом.
 */
@RequiredArgsConstructor
public class StartQuestionActionLaboratories implements ActionLaboratories {

    private final StrategyContextCombobox strategyContextCombobox;
    private final StrategyContextText strategyContextText;
    private final Button startQuestion;
    private final ComboboxConfigurator comboboxConfigurator = ComboboxConfigurator.getInstance();

    /**
     * Точка запуска логики
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(startQuestion, event -> {

            var value = strategyContextCombobox.getCombobox().getValue();
            var lastClickedButton = strategyContextCombobox.getButtonClickListener().getLastClickedButton();

            if (value != null && lastClickedButton != null) {

                var classLaboratory = comboboxConfigurator.getKeyButton(lastClickedButton.getText());
                var inputData = strategyContextText.inputArgs().getText();
                var comboboxData = value.split("\\s+")[0];

                strategyContextText.output().setText((String) ConsoleReader.executeTask(classLaboratory, comboboxData, inputData));

            }
        });
    }
}
