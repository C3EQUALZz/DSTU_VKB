package programmingLanguagesJava.laboratories.GUI.config;

import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.input.MouseEvent;
import javafx.scene.media.AudioClip;

import java.util.Objects;

public class ButtonConfigurator {
    public final AudioClip hoverClip = new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toExternalForm());
    public final AudioClip clickClip = new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toExternalForm());


    /**
     * Настройка кнопки с определенными параметрами.
     *
     * @param button       кнопка, на которую мы хотим назначить настройку по нажатию и т.п.
     * @param eventHandler событие, которое мы хотим обработать.
     */
    public void setupButtonEvent(Button button, EventHandler<MouseEvent> eventHandler) {
        // Обработка того момента, когда мышка наводится на кнопку.
        button.setOnMouseEntered(event -> new AudioClip(Objects.requireNonNull(getClass().getResource("/music/hover.mp3")).toString()).play());

        button.setOnMouseClicked(event -> {
            new AudioClip(Objects.requireNonNull(getClass().getResource("/music/click.mp3")).toString()).play();
            eventHandler.handle(event); // Передача объекта MouseEvent в обработчике события
        });
    }
}
