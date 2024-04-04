package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.strategy;

import javafx.scene.media.MediaView;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.webViewVideo.VideoPlayer;
import lombok.RequiredArgsConstructor;

/**
 * Данный класс является одним из посредников для удобного запуска элементов UI.
 * Реализован паттерн стратегия.
 * Здесь происходит настройка видео
 */
@RequiredArgsConstructor
public class VideoPlayerActionMenu implements ActionMenu {

    private final MediaView mediaViewVideo;

    /**
     * Точка запуска
     */
    @Override
    public void execute() {
        var videoPlayer = new VideoPlayer(mediaViewVideo);
        videoPlayer.event();
    }

}

