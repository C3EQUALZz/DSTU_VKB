/**
 * Данный класс предназначен для обработки символов замены в docx
 */

package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFRun;

import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Класс NumberedUnderlineReplacer реализует интерфейс UnderlineReplacer.
 * Он заменяет подчеркивания в документе на данные из JSON.
 */
class NumberedUnderlineReplacer implements UnderlineReplacer {
    private final Iterator<String> jsonData;

    /**
     * Конструктор класса NumberedUnderlineReplacer.
     *
     * @param jsonData Данные в формате JSON, которые будут использоваться для замены подчеркиваний.
     */
    public NumberedUnderlineReplacer(HashMap<String, String> jsonData) {
        this.jsonData = convertJsonForDocument(new HashMap<>(jsonData)).values().iterator();
    }

    /**
     * Заменяет все подчеркивания в документе на данные из JSON.
     *
     * @param doc Документ, в котором будут заменены подчеркивания.
     */
    @Override
    public void replaceUnderlines(XWPFDocument doc) {
        doc.getParagraphs().forEach(xwpfParagraph ->
                xwpfParagraph.getRuns().forEach(xwpfRun ->
                        parseRow(xwpfRun, xwpfRun.getText(0))));

    }

    /**
     * Заменяет подчеркивания в тексте на данные из JSON.
     *
     * @param run Объект XWPFRun, содержащий текст.
     * @param text Текст, в котором будут заменены подчеркивания.
     */
    void parseRow(XWPFRun run, String text) {
        while (text != null && text.contains("_")) {
            text = text.replaceFirst("_+", jsonData.next());
            run.setText(text, 0);
        }
    }

    /**
     * Преобразует данные JSON в формат, подходящий для документа.
     *
     * @param jsonData Исходные данные в формате JSON.
     * @return Данные в формате JSON, преобразованные для документа.
     */
    private LinkedHashMap<String, String> convertJsonForDocument(HashMap<String, String> jsonData) {
        var result = new LinkedHashMap<String, String>();
        result.put("city", jsonData.getOrDefault("addressField", "").split(",")[4]);
        result.put("year", "2024");
        result.put("mainPerson", jsonData.getOrDefault("mainPerson", ""));
        result.put("addressField", jsonData.getOrDefault("addressField", ""));
        result.put("cost", ThreadLocalRandom.current().nextInt(45_000, 100_000) + " тыс. рублей");
        return result;
    }

}