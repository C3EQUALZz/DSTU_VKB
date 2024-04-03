/**
 * Данный участок кода предназначен для обработки событий для слайдера в лабораторных работах.
 * Он улучшает UI, поэтому вот так.
 * Гайд, по которому я делал: https://youtu.be/LMl_OZHJYC8?si=h9xxWZGc3EYMa46Z
 */
package programmingLanguagesJava.laboratories.GUI.controllers.laboratories;

import javafx.animation.TranslateTransition;
import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import javafx.util.Duration;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;

class SliderController implements ElementLaboratory {
    private final AnchorPane slider;
    private final Label openSlider, closeSlider;
    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();

    // Различные позиции Slider, я пишу не масштабируемое приложение, поэтому сдвиги по пикселям.
    private enum POSITIONS {
        ;
        private static final double MENU_CLOSED_POSITION = -500;
        private static final double MENU_OPENED_POSITION = 0;
    }

    SliderController(AnchorPane slider, Label openSlider, Label closeSlider) {
        this.openSlider = openSlider;
        this.closeSlider = closeSlider;
        this.slider = initializeSlider(slider);
    }

    /**
     * Первоначальная настройка slider
     *
     * @param slider, который мы хотим настроить
     * @return результирующий slider
     */
    private AnchorPane initializeSlider(AnchorPane slider) {
        slider.setTranslateX(POSITIONS.MENU_CLOSED_POSITION);
        configureButtonSoundEffects(openSlider);
        configureButtonSoundEffects(closeSlider);
        return slider;
    }

    /**
     * Обработчик событий при нажатии на slider (три полоски)
     */
    @Override
    public void event() {
        openSlider.setOnMouseClicked(event -> openMenu());
        closeSlider.setOnMouseClicked(event -> closeMenu());
    }

    /**
     * Настройка звука для отдельного Label, так как в Slider я использовал его, имитируя кнопку
     *
     * @param button кнопку, которую мы хотим настроить
     */
    private void configureButtonSoundEffects(Label button) {
        button.setOnMouseEntered(event -> buttonConfigurator.hoverClip.play());
    }

    /**
     * Метод, который открывает нам меню
     */
    private void openMenu() {
        buttonConfigurator.clickClip.play();
        slideMenuToPosition(POSITIONS.MENU_OPENED_POSITION);
        switchButtonVisibility(false, true);
    }

    /**
     * Метод, который прячет меню
     */
    private void closeMenu() {
        buttonConfigurator.clickClip.play();
        slideMenuToPosition(POSITIONS.MENU_CLOSED_POSITION);
        switchButtonVisibility(true, false);
    }

    /**
     * Сама анимация Slider
     *
     * @param position позиция, на которую мы хотим переместить наш Slider
     */
    private void slideMenuToPosition(double position) {
        var slide = new TranslateTransition(Duration.seconds(0.4), slider);
        slide.setToX(position);
        slide.play();
    }

    /**
     * Настройка видимости слайдера
     *
     * @param openVisible  параметр видимости для openSlider
     * @param closeVisible параметр видимости для closeSlider
     */
    private void switchButtonVisibility(boolean openVisible, boolean closeVisible) {
        openSlider.setVisible(openVisible);
        closeSlider.setVisible(closeVisible);
    }

}
