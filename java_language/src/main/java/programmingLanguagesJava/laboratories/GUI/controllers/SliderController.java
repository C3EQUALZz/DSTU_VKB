package programmingLanguagesJava.laboratories.GUI.controllers;

import javafx.animation.TranslateTransition;
import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import javafx.util.Duration;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;

public class SliderController {

    private final AnchorPane slider;
    private final Label openSlider;
    private final Label closeSlider;

    private final ButtonConfigurator buttonConfigurator = new ButtonConfigurator();

    public SliderController(AnchorPane slider, Label openSlider, Label closeSlider) {
        this.slider = slider;
        this.openSlider = openSlider;
        this.closeSlider = closeSlider;
    }

    /**
     * Настройка slider меню, которое движется справа.
     * Есть баг, что в начале почему-то сверху находится closeSlider, а не openSlider.
     * В общем, поэтому с самого начала меню закрыто, а не открыто.
     * Здесь под капотом, если что 2 кнопки, которые совпадают 1 в 1.
     */
    public void sliderEvent() {
        // Состояние закрытого меню
        slider.setTranslateX(-500);

        // Установка звука на тот момент, когда мы наводимся на кнопку меню.
        openSlider.setOnMouseEntered(event -> buttonConfigurator.hoverClip.play());

        // Установка звука на тот момент, когда мы нажимаем кнопку.
        openSlider.setOnMouseClicked(event -> {

            buttonConfigurator.clickClip.play();

            TranslateTransition slide = new TranslateTransition();
            slide.setDuration(Duration.seconds(0.4));
            slide.setNode(slider);

            slide.setToX(0);
            slide.play();

            slider.setTranslateX(-500);

            slide.setOnFinished(actionEvent -> {
                openSlider.setVisible(false);
                closeSlider.setVisible(true);
            });
        });

        closeSlider.setOnMouseEntered(event -> buttonConfigurator.hoverClip.play());

        closeSlider.setOnMouseClicked(event -> {
            buttonConfigurator.clickClip.play();

            TranslateTransition slide = new TranslateTransition();
            slide.setDuration(Duration.seconds(0.4));
            slide.setNode(slider);

            slide.setToX(-500);
            slide.play();

            slider.setTranslateX(0);

            slide.setOnFinished(actionEvent -> {
                openSlider.setVisible(true);
                closeSlider.setVisible(false);
            });
        });
    }
}
