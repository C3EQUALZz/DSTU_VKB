/**
 * Модуль, который предназначен для работы с кнопками. В основном я их часто настраиваю по звукам, сделано с той
 * целью, чтобы не дублировать код.
 *
 */

package programmingLanguagesJava.laboratories.GUI.config;

import javafx.event.EventHandler;
import javafx.scene.control.ButtonBase;
import javafx.scene.input.MouseEvent;

public class ButtonConfigurator {

    private static ButtonConfigurator instance;

    /**
     * Реализация SingleTone
     * @return возвращает наш объект, который был создан 1 раз за время действия программы
     */
    public static ButtonConfigurator getInstance() {
        if (instance == null)
            instance = new ButtonConfigurator();
        return instance;
    }

    /**
     * Настройка кнопки с определенными параметрами.
     *
     * @param button       кнопка, на которую мы хотим назначить настройку по нажатию и т.п.
     * @param eventHandler событие, которое мы хотим обработать.
     */
    public void setupButtonEvent(ButtonBase button, EventHandler<MouseEvent> eventHandler) {
        // Обработка того момента, когда мышка наводится на кнопку.
        button.setOnMouseEntered(event -> SOUND.HOVER.play());

        // Обработка того момента, когда нажали на кнопку.
        button.setOnMouseClicked(event -> {
            SOUND.CLICK.play();
            eventHandler.handle(event); // Передача объекта MouseEvent в обработчике события
        });
    }

    /**
     * Настройка кнопки с определенными параметрами.
     *
     * @param button       кнопка, на которую мы хотим назначить настройку по нажатию и т.п.
     * @param action       действие, которое мы хотим выполнить при нажатии на кнопку.
     * @param errorMessage сообщение об ошибке, если действие не удалось выполнить.
     */
    public void setupButtonEvent(ButtonBase button, CheckedConsumer action, String errorMessage) {
        EventHandler<MouseEvent> eventHandler = event -> {
            try {
                action.accept(event);
            } catch (Exception e) {
                throw new RuntimeException(errorMessage, e);
            }
        };
        setupButtonEvent(button, eventHandler);
    }


}