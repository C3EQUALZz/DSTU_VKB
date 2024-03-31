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

public class MovableAnchorPane implements ElementMenu {
    private final AnchorPane anchorPane, otherAnchorPane;
    private final TranslateTransition translateTransition;
    private final FadeTransition fadeTransition;

    // Константы для продолжительности анимаций
    private enum DURATION {
        ;
        private static final Duration TRANSLATE_DURATION = Duration.seconds(2);
        private static final Duration FADE_DURATION = Duration.seconds(0.7);
    }

    /**
     * Данный класс используется для анимации, когда пользователь ввел корректный пароль
     * @param anchorPane, который будет перемещаться
     * @param otherAnchorPane, который будет прятаться
     */
    public MovableAnchorPane(AnchorPane anchorPane, AnchorPane otherAnchorPane) {
        this.anchorPane = anchorPane;
        this.otherAnchorPane = otherAnchorPane;
        this.translateTransition = new TranslateTransition(DURATION.TRANSLATE_DURATION, anchorPane);
        this.fadeTransition = configureFadeTransition();
    }

    /**
     * Обработка событий, чтобы двигался anchorPane
     */
    @Override
    public void event() {
        var newX = anchorPane.getLayoutX() + 400;
        anchorPane.setStyle("-fx-border-color: white; -fx-border-radius: 18; -fx-background-radius: 30");
        anchorPane.setLayoutX(newX);

        // Запускаем анимации
        translateTransition.setToX(newX);
        translateTransition.play();
        fadeTransition.play();
    }

    /**
     * Метод, который проводит конфигурацию для исчезновения правого anchorPane.
     * В event такое можно сделать, но в таком случае будет переизбыток кода, поэтому вынесено в отдельный метод
     * @return возвращает настроенное исчезновение
     */
    private FadeTransition configureFadeTransition() {
        var fadeTransition = new FadeTransition(DURATION.FADE_DURATION, otherAnchorPane);
        fadeTransition.setFromValue(1.0);
        fadeTransition.setToValue(0.0);
        fadeTransition.setOnFinished(event -> otherAnchorPane.setVisible(false));
        return fadeTransition;
    }

}