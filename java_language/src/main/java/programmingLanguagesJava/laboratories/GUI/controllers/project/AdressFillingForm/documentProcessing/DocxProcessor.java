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
import java.util.Map;

import lombok.RequiredArgsConstructor;

/**
 * Класс DocxProcessor обрабатывает документы в формате DOCX.
 */
@RequiredArgsConstructor
public class DocxProcessor {

    private final String PATH_TO_PROJECT = "src/main/resources/projectFiles";
    private final Path PATH_TO_DIR = Paths.get(PATH_TO_PROJECT, "documents_for_database").toAbsolutePath();
    private final Path PATH_BLANK = Paths.get(PATH_TO_PROJECT, "blank-dogovora-okazanija-ohrannyh-uslug.docx").toAbsolutePath();

    private final Map<String, String> jsonData;
    private volatile String result;


    /**
     * Метод event() обрабатывает документ, заменяя подчеркивания на данные из JSON.
     *
     * @return Путь к обработанному документу.
     * @throws RuntimeException Если произошла ошибка при обработке документа.
     */
    public String event() {

        new Thread(() -> {
            try {
                var originalDoc = openOriginalDoc();

                var replacer = new NumberedUnderlineReplacer(this.jsonData);
                replacer.replaceUnderlines(originalDoc);

                var newFilePath = createNewDocx();

                saveResult(originalDoc, newFilePath);

                // Сохраняем результат в общей переменной
                result = newFilePath;

            } catch (Exception e) {
                throw new RuntimeException("Ошибка при обработке документа", e);
            }
        }).start();

        return result;
    }

    /**
     * Метод openOriginalDoc() открывает файл с примером договора в формате XWPFDocument.
     *
     * @return XWPFDocument - объект, представляющий открытый файл с примером договора.
     * @throws RuntimeException если не удалось открыть файл с примером договора.
     */
    private XWPFDocument openOriginalDoc() {

        try {

            var fis = new FileInputStream(PATH_BLANK.toFile());
            return new XWPFDocument(new BufferedInputStream(fis));

        } catch (IOException e) {

            throw new RuntimeException("Не получилось открыть файл с примером договора", e);

        }

    }

    /**
     * Метод saveResult() сохраняет измененный документ в формате XWPFDocument по указанному пути.
     *
     * @param doc XWPFDocument - объект, представляющий измененный документ.
     * @param filePath String - путь, по которому следует сохранить измененный документ.
     * @throws RuntimeException если не удалось сохранить результат изменения в документ.
     */
    private void saveResult(XWPFDocument doc, String filePath) {

        try (var fos = new BufferedOutputStream(new FileOutputStream(filePath))) {

            doc.write(fos);

        } catch (IOException e) {

            throw new RuntimeException("Не получилось сохранить результат изменения в документ", e);

        }
    }

    /**
     * Метод createNewDocx() создает новый документ в формате DOCX с указанным именем.
     * Имя файла формируется на основе базового имени и расширения файла.
     *
     * @return String - путь к созданному временному файлу в формате DOCX.
     * @throws RuntimeException если возникает ошибка при создании нового файла.
     */
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
