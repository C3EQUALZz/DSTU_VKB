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

/**
 * Класс, который описывает считыватель файла из БД.
 * Он позволяет просматривать информацию.
 */
@RequiredArgsConstructor
public class Reader implements ElementDatabaseView {

    private final TableView<PersonInfo> customersTableView;
    private final Button button;
    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();

    /**
     * Здесь стоит точка на тот момент, когда пользователь нажимает кнопку создать документ
     */
    @Override
    public void event() {
        buttonConfigurator.setupButtonEvent(button, mouseEvent -> {

            PersonInfo selectedPerson = customersTableView.getSelectionModel().getSelectedItem();
            openDocument(selectedPerson.getDocument());

        });
    }

    /**
     * Метод, который открывает документ, чтобы можно было его просматривать.
     * @param document байтовый массив, который описывает документ.
     */
    private void openDocument(byte[] document) {
        try {
            Path tempPath = Files.createTempFile("document", ".docx");
            File tempFile = tempPath.toFile();
            tempFile.deleteOnExit();

            try (FileOutputStream fos = new FileOutputStream(tempFile)) {
                fos.write(document);
            }


            Desktop.getDesktop().open(tempFile);
        } catch (IOException e) {
            throw new RuntimeException("Не получилось открыть docx файл", e);
        }
    }
}
