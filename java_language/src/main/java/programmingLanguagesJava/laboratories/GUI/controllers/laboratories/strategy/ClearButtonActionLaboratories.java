package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategy;

import javafx.scene.control.Button;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext.StrategyContextText;

/**
 * Класс, который является связкой и настройкой для кнопки, чтобы очищать данные после ввода пользователя
 */
@RequiredArgsConstructor
public class ClearButtonActionLaboratories implements ActionLaboratories {

    private final StrategyContextText strategyContextText;
    private final Button clearInput;

    /**
     * Точка запуска кода
     */
    @Override
    public void execute() {
        buttonConfigurator.setupButtonEvent(clearInput, event -> {
            strategyContextText.condition().clear();
            strategyContextText.inputArgs().clear();
            strategyContextText.output().clear();
        });
    }
}
