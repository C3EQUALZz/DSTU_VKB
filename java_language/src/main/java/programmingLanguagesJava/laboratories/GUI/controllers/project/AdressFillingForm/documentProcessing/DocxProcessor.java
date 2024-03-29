/**
 * Здесь лежит копия документа https://assistentus.ru/forma/dogovor-okazaniya-ohrannyh-uslug/view
 * Реализован паттерн Стратегия для улучшения поддержки кода, соблюдения SOLID
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing;

import org.apache.poi.xwpf.usermodel.XWPFDocument;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;

public class DocxProcessor {
    private final String PATH_TO_PROJECT = "src/main/resources/projectFiles";
    private final Path PATH_TO_DIR = Paths.get(PATH_TO_PROJECT, "documents_for_database").toAbsolutePath();
    private final Path PATH_BLANK = Paths.get(PATH_TO_PROJECT, "blank-dogovora-okazanija-ohrannyh-uslug.docx").toAbsolutePath();

    private final HashMap<String, String> jsonData;

    public DocxProcessor(HashMap<String, String> jsonData) {
        this.jsonData = jsonData;
    }

    public String event() {
        try {
            var originalDoc = openOriginalDoc();

            var replacer = new NumberedUnderlineReplacer(this.jsonData);
            replacer.replaceUnderlines(originalDoc);

            var newFilePath = createNewDocx();

            saveResult(originalDoc, newFilePath);

            return newFilePath;

        } catch (Exception e) {
            throw new RuntimeException("Ошибка при обработке документа", e);
        }
    }

    private XWPFDocument openOriginalDoc() {

        try {

            var fis = new FileInputStream(PATH_BLANK.toFile());
            return new XWPFDocument(new BufferedInputStream(fis));

        } catch (IOException e) {

            throw new RuntimeException("Не получилось открыть файл с примером договора", e);

        }

    }

    private void saveResult(XWPFDocument doc, String filePath) {

        try (BufferedOutputStream fos = new BufferedOutputStream(new FileOutputStream(filePath))) {

            doc.write(fos);

        } catch (IOException e) {

            throw new RuntimeException("Не получилось сохранить результат изменения в документ", e);

        }
    }

    private String createNewDocx() {

        final var NAME_OF_FILE = "blank-dogovora-okazanija-ohrannyh-uslug.docx";
        var baseName = NAME_OF_FILE.substring(0, NAME_OF_FILE.lastIndexOf('.'));
        var extension = NAME_OF_FILE.substring(NAME_OF_FILE.lastIndexOf('.'));

        try {

            Files.createDirectories(PATH_TO_DIR);
            return Files.createTempFile(PATH_TO_DIR, baseName + "-", extension).toAbsolutePath().toString();

        } catch (IOException e) {

            throw new RuntimeException("Ошибка создания нового файла", e);

        }

    }
}
