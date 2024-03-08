package programmingLanguagesJava.laboratories.GUI.controllers.project.AdressFillingForm.documentProcessing;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFRun;

class NumberedUnderlineReplacer implements UnderlineReplacer {
    private int count = 0;

    @Override
    public void replaceUnderlines(XWPFDocument doc) {
        for (var paragraph : doc.getParagraphs()) {
            for (var run : paragraph.getRuns()) {
                parseRow(run, run.getText(0), count);
            }
        }
    }

    void parseRow(XWPFRun run, String text, int count) {
        while (text != null && text.contains("_")) {
            text = text.replaceFirst("_+", String.valueOf(count++));
            run.setText(text, 0);
        }
    }
}
