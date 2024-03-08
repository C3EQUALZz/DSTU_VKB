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

public class DocxProcessor {
    private static final String PATH_TO_PROJECT = "java_language/src/main/resources/projectFiles";
    private static final String NAME_OF_FILE = "blank-dogovora-okazanija-ohrannyh-uslug.docx";
    private static final Path PATH_TO_DIR = Paths.get(PATH_TO_PROJECT, "documents_for_database");
    private static final Path PATH_BLANK = Paths.get(PATH_TO_PROJECT, "blank-dogovora-okazanija-ohrannyh-uslug.docx");

    public String event() {
        try {
            var originalDoc = openOriginalDoc();

            var replacer = new NumberedUnderlineReplacer();
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

            var fis = new FileInputStream(DocxProcessor.PATH_BLANK.toFile());
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
