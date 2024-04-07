package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readingPhotoFromDatabase;

import javafx.scene.control.Button;
import javafx.scene.control.TableView;
import lombok.RequiredArgsConstructor;

import java.awt.Desktop;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;

@RequiredArgsConstructor
public class PhotoReader implements ElementDatabaseView {

    private final TableView<PersonInfo> customersTableView;
    private final Button button;
    private final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();

    @Override
    public void event() {
        buttonConfigurator.setupButtonEvent(button, mouseEvent -> {

            PersonInfo selectedPerson = customersTableView.getSelectionModel().getSelectedItem();
            openPhoto(selectedPerson.getPlanOfHouse());

        });
    }

    private void openPhoto(byte[] photo) {
        try {
            // Создаем временный файл
            Path tempFile = Files.createTempFile("photo", ".png");

            // Записываем массив байтов в файл
            Files.write(tempFile, photo, StandardOpenOption.WRITE);

            if (Desktop.isDesktopSupported()) {
                try {
                    Desktop.getDesktop().open(tempFile.toFile());
                } catch (IOException e) {
                    throw new RuntimeException("Данная платформа не позволяет открывать файлы", e);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException("Ошибка при создании временного файла", e);
        }
    }
}
