package programmingLanguagesJava.laboratories.GUI.fileObserver;

import java.io.IOException;
import java.nio.file.*;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import javafx.application.Platform;


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

    private WatchService setupWatchService() throws IOException {
        var watchService = FileSystems.getDefault().newWatchService();
        Paths.get(fileReaderService.getFILE_PATH()).getParent().register(watchService, StandardWatchEventKinds.ENTRY_MODIFY);
        return watchService;
    }


    private void handleEvents(WatchKey key) {
        for (WatchEvent<?> event : key.pollEvents()) {
            if (event.kind() == StandardWatchEventKinds.ENTRY_MODIFY) {
                handleModifyEvent();
            }
        }
    }

    private void handleModifyEvent() {
        var message = fileReaderService.readWordFromFile();
        if (message != null && WORDS.contains(message.trim().toLowerCase())) {
            Platform.runLater(alertService::createAlert);
        }
    }
}
