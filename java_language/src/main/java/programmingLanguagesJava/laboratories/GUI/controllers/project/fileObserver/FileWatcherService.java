package programmingLanguagesJava.laboratories.GUI.controllers.project.fileObserver;

import java.io.IOException;
import java.nio.file.*;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import javafx.application.Platform;


/**
 * Здесь собрана логика просмотра файла, который позволяет отслеживать изменения.
 * Написан он не лучшим образом, потому что надо было сделать внедрение зависимостей по словам.
 * Мне же уже не хочется многое что исправлять, так как хочу быстрее сдать проект.
 */
public class FileWatcherService extends Thread {

    private final Set<String> WORDS = new HashSet<>(Arrays.asList(
            "кража", "украли", "обокрали", "взломали", "взлом",
            "стырили", "красть", "ломать", "стырить"
    ));

    private final FileReaderService fileReaderService;
    private final AlertService alertService;


    public FileWatcherService() {
        this.fileReaderService = new FileReaderService();
        this.alertService = new AlertService();
    }

    /**
     * Точка запуска отдельного потока, который просматривает файл.
     */
    @Override
    public void run() {
        try (var watchService = setupWatchService()) {

            while (!isInterrupted()) {
                var key = watchService.take();
                handleEvents(key);
                key.reset();
            }

        } catch (IOException | InterruptedException e) {

            throw new RuntimeException("Не получилось найти файл", e);

        }
    }

    /**
     * Этот метод настраивает службу наблюдения за файлами.
     * @return возвращает WatchService, который помогает отслеживать
     * @throws IOException бросает исключение, если получилось вызвать слушателя от операционной системы
     */
    private WatchService setupWatchService() throws IOException {
        var watchService = FileSystems.getDefault().newWatchService();
        Paths.get(fileReaderService.getFILE_PATH()).getParent().register(watchService, StandardWatchEventKinds.ENTRY_MODIFY);
        return watchService;
    }

    /**
     * Здесь достаточно много event-ов можно отслеживать, а я фильтрую, что именно изменение файла.
     */
    private void handleEvents(WatchKey key) {
        for (WatchEvent<?> event : key.pollEvents()) {
            if (event.kind() == StandardWatchEventKinds.ENTRY_MODIFY) {
                handleModifyEvent();
            }
        }
    }

    /**
     * Этот метод вызывается, когда файл, за которым наблюдает служба, изменяется.
     * Здесь уже идет проверка на ключевые слова.
     */
    private void handleModifyEvent() {
        var message = fileReaderService.readWordFromFile();
        if (message != null && WORDS.contains(message.trim().toLowerCase())) {
            Platform.runLater(alertService::start);
        }
    }
}
