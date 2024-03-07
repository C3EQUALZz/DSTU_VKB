/**
 * Здесь лежит копия документа https://assistentus.ru/forma/dogovor-okazaniya-ohrannyh-uslug/view
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFRun;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class DocxProcessor {
    private static final String PATH_TO_PROJECT = "java_language/src/main/resources/projectFiles";
    private static final Path PATH_TO_DIR = Paths.get(PATH_TO_PROJECT, "documents_for_database");
    private static final Path PATH_BLANK = Paths.get(PATH_TO_PROJECT, "blank-dogovora-okazanija-ohrannyh-uslug.docx");

    public static void main(String[] args) {
        try {
            var originalDoc = openOriginalDoc(PATH_BLANK);

            replaceUnderlines(originalDoc);

            var newFilePath = createNewDocx("blank-dogovora-okazanija-ohrannyh-uslug.docx");
            saveResult(originalDoc, newFilePath);

            System.out.println("Замена завершена успешно!");
        } catch (Exception e) {
            throw new RuntimeException("Ошибка при обработке документа", e);
        }
    }

    private static XWPFDocument openOriginalDoc(Path filePath) throws IOException {
        var fis = new FileInputStream(filePath.toFile());
        return new XWPFDocument(new BufferedInputStream(fis));
    }

    private static void replaceUnderlines(XWPFDocument doc) {
        var count = 0;
        for (var paragraph : doc.getParagraphs()) {
            for (var run : paragraph.getRuns()) {
                parseRow(run, run.getText(0), count);
            }
        }
    }

    private static void parseRow(XWPFRun run, String text, int count) {
        while (text != null && text.contains("_")) {
            text = text.replaceFirst("_+", String.valueOf(count++));
            run.setText(text, 0);
        }
    }

    private static void saveResult(XWPFDocument doc, String filePath) throws IOException {
        try (BufferedOutputStream fos = new BufferedOutputStream(new FileOutputStream(filePath))) {
            doc.write(fos);
        }
    }

    private static String createNewDocx(String fileName) {
        var baseName = fileName.substring(0, fileName.lastIndexOf('.'));
        var extension = fileName.substring(fileName.lastIndexOf('.'));

        try {

            Files.createDirectories(PATH_TO_DIR);
            return Files.createTempFile(PATH_TO_DIR, baseName + "-", extension).toAbsolutePath().toString();

        } catch (IOException e) {

            throw new RuntimeException("Ошибка создания нового файла", e);

        }

    }
}
