/**
 * Данный участок кода предназначен для обработки событий для слайдера в лабораторных работах.
 * Он улучшает UI, поэтому вот так.
 *
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
        this.slider = slider;
        this.openSlider = openSlider;
        this.closeSlider = closeSlider;
        initializeSlider();
    }
    @Override
    public void event() {
        openSlider.setOnMouseClicked(event -> openMenu());
        closeSlider.setOnMouseClicked(event -> closeMenu());
    }

    private void initializeSlider() {
        slider.setTranslateX(POSITIONS.MENU_CLOSED_POSITION);
        configureButtonSoundEffects(openSlider);
        configureButtonSoundEffects(closeSlider);
    }

    private void configureButtonSoundEffects(Label button) {
        button.setOnMouseEntered(event -> buttonConfigurator.hoverClip.play());
    }

    private void openMenu() {
        buttonConfigurator.clickClip.play();
        slideMenuToPosition(POSITIONS.MENU_OPENED_POSITION);
        switchButtonVisibility(false, true);
    }

    private void closeMenu() {
        buttonConfigurator.clickClip.play();
        slideMenuToPosition(POSITIONS.MENU_CLOSED_POSITION);
        switchButtonVisibility(true, false);
    }

    private void slideMenuToPosition(double position) {
        var slide = new TranslateTransition(Duration.seconds(0.4), slider);
        slide.setToX(position);
        slide.play();
    }

    private void switchButtonVisibility(boolean openVisible, boolean closeVisible) {
        openSlider.setVisible(openVisible);
        closeSlider.setVisible(closeVisible);
    }

}
