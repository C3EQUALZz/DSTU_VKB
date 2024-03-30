package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.webViewVideo;

import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.ElementMenu;

import java.io.File;

public class VideoPlayer implements ElementMenu {
    private final MediaView mediaView;

    public VideoPlayer(MediaView mediaView) {
        this.mediaView = mediaView;
    }

    @Override
    public void event() {
        var media = new Media(getPathToFile());
        var mediaPlayer = new MediaPlayer(media);
        mediaView.setMediaPlayer(mediaPlayer);
        mediaPlayer.play();
    }

    private String getPathToFile() {
        // Получаем текущий рабочий каталог проекта
        var currentDirectory = System.getProperty("user.dir");

        // Относительный путь к видеофайлу
        var relativePath = "src/main/resources/projectFiles/video/camera.mp4";

        // Создаем объект File с использованием текущего каталога и относительного пути
        var file = new File(currentDirectory, relativePath);

        // Получаем абсолютный путь к файлу
        return file.toURI().toString();
    }
}
