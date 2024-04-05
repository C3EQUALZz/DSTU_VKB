package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategy;

import javafx.scene.control.Button;
import javafx.scene.input.MouseEvent;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext.StrategyContextCombobox;

import java.util.stream.Stream;

/**
 * Данный класс реализовывает настройку для каждой кнопки, здесь происходит настройка звука,
 * установка слушателя на нажатие кнопки.
 * Здесь ещё есть костыль с combobox, который включает его при нажатии на любую кнопку.
 */
@RequiredArgsConstructor
public class ButtonLabsActionLaboratories implements ActionLaboratories {
    private final StrategyContextCombobox strategyContextCombobox;
    private final Stream<Button> buttonStream;

    /**
     * Метод, который запускает настройку для каждой кнопки
     */
    @Override
    public void execute() {
        buttonStream.forEach(this::setupButton);
    }

    /**
     * Настройка отдельной кнопки
     * @param button кнопка, которую мы хотим настроить
     */
    private void setupButton(Button button) {
        buttonConfigurator.setupButtonEvent(button, strategyContextCombobox.getButtonClickListener());
        button.addEventHandler(MouseEvent.MOUSE_CLICKED, event -> strategyContextCombobox.getCombobox().setDisable(false));
    }
}
