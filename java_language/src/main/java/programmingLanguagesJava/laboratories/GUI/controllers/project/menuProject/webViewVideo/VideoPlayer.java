/**
 * Данный пакет символизирует запись с камеры, которая происходит в округе
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.webViewVideo;

import javafx.application.Platform;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import programmingLanguagesJava.laboratories.GUI.controllers.project.menuProject.ElementMenu;
import lombok.RequiredArgsConstructor;

import java.io.File;

@RequiredArgsConstructor
public class VideoPlayer implements ElementMenu {
    private final MediaView mediaView;

    /**
     * Запуск видео происходит здесь
     */
    @Override
    public void event() {
        new Thread(() -> {

            try {
                Thread.sleep(1000); // Задержка в 1 секунду
            } catch (InterruptedException e) {
                throw new RuntimeException("не получился костыль с видео :)", e);
            }

            var media = new Media(getPathToFile());
            var mediaPlayer = new MediaPlayer(media);
            mediaPlayer.setAutoPlay(true);

            mediaPlayer.setOnReady(() -> Platform.runLater(() -> {
                mediaView.setMediaPlayer(mediaPlayer);
                mediaPlayer.play();
            }));

            mediaPlayer.setOnError(() -> System.out.println("Ошибка при воспроизведении видео: " + mediaPlayer.getError()));
        }).start();
    }



    /**
     * Получение абсолютного пути до файла с нашего видео
     * @return путь к видео
     */
    private String getPathToFile() {
        var currentDirectory = System.getProperty("user.dir");
        var relativePath = "src/main/resources/projectFiles/video/camera.mp4";
        var file = new File(currentDirectory, relativePath);
        return file.toURI().toString();
    }
}
