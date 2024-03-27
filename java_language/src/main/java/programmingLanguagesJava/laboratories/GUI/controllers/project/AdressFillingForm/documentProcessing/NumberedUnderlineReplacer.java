package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFRun;

import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.concurrent.ThreadLocalRandom;

class NumberedUnderlineReplacer implements UnderlineReplacer {
    private final Iterator<String> jsonData;

    public NumberedUnderlineReplacer(HashMap<String, String> jsonData) {
        this.jsonData = convertJsonForDocument(jsonData).values().iterator();
    }

    @Override
    public void replaceUnderlines(XWPFDocument doc) {
        doc.getParagraphs().forEach(xwpfParagraph ->
                xwpfParagraph.getRuns().forEach(xwpfRun ->
                        parseRow(xwpfRun, xwpfRun.getText(0))));

    }

    void parseRow(XWPFRun run, String text) {
        while (text != null && text.contains("_")) {
            text = text.replaceFirst("_+", jsonData.next());
            run.setText(text, 0);
        }
    }


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