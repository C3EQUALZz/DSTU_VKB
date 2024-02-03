package programmingLanguagesJava.laboratories.GUI.config.ParserLabs;

import com.ibm.icu.text.RuleBasedNumberFormat;

import java.lang.reflect.Method;
import java.text.ParseException;
import java.util.Comparator;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class StringNumberComparator implements Comparator<Method> {

    @Override
    public int compare(Method o1, Method o2) {
        return Integer.compare(numberFromString(o1.getName()), numberFromString(o2.getName()));
    }

    private int numberFromString(String number) {

        RuleBasedNumberFormat numberFormat = new RuleBasedNumberFormat(Locale.UK, RuleBasedNumberFormat.SPELLOUT);
        try {
            return numberFormat.parse(parseToUnderstandableForm(number)).intValue();
        } catch (ParseException e) {
            return -1;
        }
    }

    private String parseToUnderstandableForm(String numberWithQuestion) {

        var number = numberWithQuestion.substring(0, numberWithQuestion.indexOf("Q") + 1);

        Pattern pattern = Pattern.compile("[A-Z]");
        Matcher matcher = pattern.matcher(number);

        if (matcher.find()) {
            var charUpper = matcher.group();

            return number.replace(charUpper, "-"+charUpper.toUpperCase());
        }

        return number;
    }

}
