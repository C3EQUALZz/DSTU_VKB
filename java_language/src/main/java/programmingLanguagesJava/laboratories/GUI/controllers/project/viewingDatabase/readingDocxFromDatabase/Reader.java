package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readingDocxFromDatabase;

import javafx.scene.control.Button;
import javafx.scene.control.TableView;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;
import lombok.RequiredArgsConstructor;

import java.awt.*;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

@RequiredArgsConstructor
public class Reader implements ElementDatabaseView {

    private final TableView<PersonInfo> customersTableView;
    private final Button button;
    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();

    @Override
    public void event() {
        buttonConfigurator.setupButtonEvent(button, mouseEvent -> {

            PersonInfo selectedPerson = customersTableView.getSelectionModel().getSelectedItem();
            openDocument(selectedPerson.getDocument());

        });
    }

    private void openDocument(byte[] document) {
        try {
            // Создание временного файла
            Path tempPath = Files.createTempFile("document", ".docx");
            File tempFile = tempPath.toFile();
            tempFile.deleteOnExit(); // Удаление файла при выходе из программы

            // Запись blob в файл
            try (FileOutputStream fos = new FileOutputStream(tempFile)) {
                fos.write(document);
            }

            // Открытие файла с помощью приложения по умолчанию
            Desktop.getDesktop().open(tempFile);
        } catch (IOException e) {

            throw new RuntimeException("Не получилось открыть docx файл", e);
        }
    }
}
