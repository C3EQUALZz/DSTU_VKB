package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject;

import javafx.animation.TranslateTransition;
import javafx.scene.layout.AnchorPane;
import javafx.util.Duration;

class MovableAnchorPane implements ElementMenu {
    private final AnchorPane anchorPane;
    private final TranslateTransition translateTransition;

    MovableAnchorPane(AnchorPane anchorPane) {
        this.anchorPane = anchorPane;
        this.translateTransition = new TranslateTransition(Duration.seconds(2), anchorPane);
    }

    @Override
    public void event() {
        this.translateTransition.setToX(anchorPane.getLayoutX() * 400);
        this.translateTransition.play();
    }

}
