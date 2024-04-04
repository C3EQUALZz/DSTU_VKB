/**
 * Интерфейс, который позволяет связывать элементы UI
 * Здесь default используется, так как в некоторых местах принимается event(),
 * а в одном месте с MouseEvent
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm;

import javafx.scene.input.MouseEvent;

public interface ElementAddressFillingForm {
    default void event() {}
    default void event(MouseEvent event) {}
}
