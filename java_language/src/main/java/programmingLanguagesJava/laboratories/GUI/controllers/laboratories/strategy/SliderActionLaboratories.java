package programmingLanguagesJava.laboratories.GUI.controllers.laboratories.strategy;

import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import lombok.AllArgsConstructor;
import programmingLanguagesJava.laboratories.GUI.controllers.laboratories.SliderController;

/**
 * Класс, который также является прослойкой между запуском и реализацией элементов UI.
 * Здесь происходит запуск слайдера (слева меню, которое двигается)
 */
@AllArgsConstructor
public class SliderActionLaboratories implements ActionLaboratories {

    private Label openSlider, closeSlider;
    private AnchorPane slider;

    /**
     * Запуск логики обработки слайдера
     */
    @Override
    public void execute() {
        new SliderController(slider, openSlider, closeSlider).event();
    }
}
