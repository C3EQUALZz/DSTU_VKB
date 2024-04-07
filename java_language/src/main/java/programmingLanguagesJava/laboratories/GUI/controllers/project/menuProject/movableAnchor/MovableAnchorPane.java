/**
 * Данный класс направлен на левую часть меню, где есть заставка с компанией.
 * Нужно было как-то разнообразить меню, поэтому сделал анимацию такую, чтобы можно было поместить элементы.
 * За идею брал отсюда: https://youtu.be/SKyDoyAZyOo?si=xdOgZrXaQpxbtl4t
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.movableAnchor;

import javafx.animation.FadeTransition;
import javafx.animation.TranslateTransition;
import javafx.scene.layout.AnchorPane;
import javafx.util.Duration;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.ElementMenu;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.strategyContext.ContextAnchorPane;

public class MovableAnchorPane implements ElementMenu {

    private final AnchorPane anchorPane, registrationAnchorPane, cameraAnchorPane;

    // Константы для продолжительности анимаций
    private enum DURATION {
        ;
        private static final Duration TRANSLATE_DURATION = Duration.seconds(2);
        private static final Duration FADE_DURATION = Duration.seconds(2);
    }

    /**
     * Данный класс используется для анимации, когда пользователь ввел корректный пароль
     */
    public MovableAnchorPane(ContextAnchorPane contextAnchorPane) {
        this.anchorPane = contextAnchorPane.anchorPaneMovable();
        this.registrationAnchorPane = contextAnchorPane.registrationAnchorPane();
        this.cameraAnchorPane = contextAnchorPane.hiddenAnchorPane();
    }

    /**
     * Обработка событий, чтобы двигался anchorPane
     */
    @Override
    public void event() {
        var newX = anchorPane.getLayoutX() + 400;
        anchorPane.setStyle("-fx-border-color: white; -fx-border-radius: 18; -fx-background-radius: 30");
        anchorPane.setLayoutX(newX);


        var translateTransition = new TranslateTransition(DURATION.TRANSLATE_DURATION, anchorPane);
        translateTransition.setToX(newX);
        translateTransition.play();

        configureFadeTransition(registrationAnchorPane, 1.0, 0.0, false).play();
        configureFadeTransition(cameraAnchorPane, 0.0, 1.0, true).play();
    }

    /**
     * Метод, который проводит конфигурацию для исчезновения правого anchorPane.
     * В event такое можно сделать, но в таком случае будет переизбыток кода, поэтому вынесено в отдельный метод
     * @return возвращает настроенное исчезновение
     */
    private FadeTransition configureFadeTransition(AnchorPane pane, double fromValue, double toValue, boolean visibility) {
        var fadeTransition = new FadeTransition(DURATION.FADE_DURATION, pane);
        fadeTransition.setFromValue(fromValue);
        fadeTransition.setToValue(toValue);
        fadeTransition.setOnFinished(event -> pane.setVisible(visibility));
        return fadeTransition;
    }

}