package programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.readersFromDatabase;

import javafx.scene.control.Button;
import javafx.scene.control.TableView;
import programmingLanguagesJava.laboratories.GUI.config.ButtonConfigurator;
import programmingLanguagesJava.laboratories.GUI.controllers.project.database.utils.PersonInfo;
import programmingLanguagesJava.laboratories.GUI.controllers.project.viewingDatabase.ElementDatabaseView;

import java.awt.*;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;

import lombok.RequiredArgsConstructor;

/**
 * Абстрактный класс, который позволяет настроить открытия файлов из БД, расширяет возможности открытия файлов.
 */
@RequiredArgsConstructor
public abstract class FileOpener implements ElementDatabaseView {

    protected final TableView<PersonInfo> customersTableView;
    protected final Button button;
    protected final ButtonConfigurator buttonConfigurator = ButtonConfigurator.getInstance();


    /**
     * Метод, который позволяет создавать временные файл для просмотра фото или Word документов.
     * Сам процесс открытия делается за счет Desktop, который сам определяет возможные приложения.
     * @param fileContent массив байтов из базы данных, который мы достали
     * @param extension расширение файла, в которое мы временно хотим создать.
     */
    protected void openFile(byte[] fileContent, String extension) {
        try {

            var tempFile = Files.createTempFile("document", extension).toFile();

            tempFile.deleteOnExit();

            try (FileOutputStream fos = new FileOutputStream(tempFile)) {
                fos.write(fileContent);
            }

            Desktop.getDesktop().open(tempFile);
        } catch (IOException e) {
            throw new RuntimeException("Ошибка при открытии файла", e);
        }
    }
}
