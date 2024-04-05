package programmingLanguagesJava.laboratories.GUI.controllers.laboratories;

import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.input.MouseEvent;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.config.ComboboxConfigurator;

/**
 * Здесь класс, который реализует паттерн слушателя.
 * Здесь реализуется EventHandler, чтобы активно вызывался handle.
 * Реализован с той целью, чтобы отслеживать последнюю кнопку.
 */
@Getter
@RequiredArgsConstructor
public class ButtonClickListener implements EventHandler<MouseEvent> {

    private Button lastClickedButton = null;
    private final ComboBox<String> combobox;
    private final ComboboxConfigurator comboboxConfigurator = ComboboxConfigurator.getInstance();

    /**
     * Запуск самой логики отслеживания, тут именно накладывается и конфигурируется кнопка.
     * @param event the event which occurred
     */
    @Override
    public void handle(MouseEvent event) {
        lastClickedButton = (Button) event.getSource();
        comboboxConfigurator.setupComboboxEvent(combobox, lastClickedButton);
    }

}


