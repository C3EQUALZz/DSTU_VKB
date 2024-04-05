package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategyContext;
import javafx.scene.control.ComboBox;
import lombok.Getter;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.ButtonClickListener;

/**
 * Класс, который является логическим объединением, повторяющихся элементов в аргументах.
 * В основном, он как вспомогательный, который сокращает количество передаваемых аргументов.
 */
@Getter
public class StrategyContextCombobox {
    private final ButtonClickListener buttonClickListener;
    private final ComboBox<String> combobox;

    public StrategyContextCombobox(ComboBox<String> combobox) {
        this.combobox = combobox;
        this.buttonClickListener = new ButtonClickListener(combobox);
    }

}
