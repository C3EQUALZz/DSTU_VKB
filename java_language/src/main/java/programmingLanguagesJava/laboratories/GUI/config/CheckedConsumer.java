/**
 * Функциональный интерфейс, который позволяет вам бросать исключения без явного использования try-catch
 */

package programmingLanguagesJava.laboratories.GUI.config;

import javafx.scene.input.MouseEvent;

@FunctionalInterface
public interface CheckedConsumer {
    void accept(MouseEvent t) throws Exception;
}
