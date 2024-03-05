/**
 * Здесь лежит копия документа https://assistentus.ru/forma/dogovor-okazaniya-ohrannyh-uslug/view
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.stream.IntStream;

public class DocxProcessor {

    private static final String FILE_PATH = "projectFiles/blank-dogovora-okazanija-ohrannyh-uslug.docx";
    private static final String MODIFIED_PATH = "projectFiles/blank-dogovora-okazanija-ohrannyh-uslug-1.docx";
    private static final InputStream FULL_PATH = DocxProcessor.class.getClassLoader().getResourceAsStream(FILE_PATH);

    public static void main(String[] args) {
        replaceTextInDocx();
    }


    public static void replaceTextInDocx() {

        if (FULL_PATH == null) {
            throw new RuntimeException("Ничего нет по данному файлу");
        }

        try (var document = new XWPFDocument(FULL_PATH)) {

            saveNewDocument(parseDocument(document));

        } catch (IOException e) {

            throw new RuntimeException("Ошибка обработки документа", e);

        }
    }

    private static XWPFDocument parseDocument(XWPFDocument document) {

        document.getParagraphs().forEach(paragraph -> {
            var text = paragraph.getText();

            if (text.contains("_______")) {
                replaceTextInParagraph(paragraph, "Your Replacement Text");
            }

        });

        return document;

    }

    private static void replaceTextInParagraph(XWPFParagraph paragraph, String replacementText) {
        // Очистим содержимое параграфа
        IntStream.iterate(-1, i -> i - 1).limit(paragraph.getRuns().size() - 1).forEach(paragraph::removeRun);
        // Добавим новый текст
        paragraph.createRun().setText(replacementText);
    }

    private static void saveNewDocument(XWPFDocument document) throws IOException {
        try (FileOutputStream fos = new FileOutputStream(MODIFIED_PATH)) {

            document.write(fos);

        } catch (IOException e) {

            throw new RuntimeException("Не получилось записать в файл", e);

        }

    }
}
