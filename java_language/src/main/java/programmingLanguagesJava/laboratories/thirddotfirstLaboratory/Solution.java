package programmingLanguagesJava.laboratories.thirddotfirstLaboratory;

import programmingLanguagesJava.laboratories.ConsoleReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Solution {
    public static void main(String[] args) {
        // System.out.println(ConsoleReader.executeTask(Solution.class));
    }

    /**
     * 1. Написать регулярное выражение, определяющее является ли данная строка строкой "abcdefghijklmnopqrstuv18340" или нет.
     * – пример правильных выражений: abcdefghijklmnopqrstuv18340.
     * – пример неправильных выражений: abcdefghijklmnoasdfasdpqrstuv18340.
     */
    @SuppressWarnings("unused")
    public String firstQuestion(String string) {
        return String.valueOf(Pattern.matches("abcdefghijklmnopqrstuv18340", string.strip()));
    }

    /**
     * 2. Написать регулярное выражение, определяющее является ли данная строка GUID с или без скобок.
     * Где GUID это строчка, состоящая из 8, 4, 4, 4, 12 шестнадцатеричных цифр разделенных тире.
     * – пример правильных выражений: e02fd0e4-00fd-090A-ca30-0d00a0038ba0.
     * – пример неправильных выражений: e02fd0e400fd090Aca300d00a0038ba0.
     */
    @SuppressWarnings("unused")
    public String secondQuestion(String string) {
        return String.valueOf(Pattern.matches("^(\\{?[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}}?)$", string.strip()));
    }

    /**
     * 3. Написать регулярное выражение, определяющее является ли заданная строка правильным MAC-адресом.
     * – пример правильных выражений: aE:dC:cA:56:76:54.
     * – пример неправильных выражений: 01:23:45:67:89:Az.
     */
    @SuppressWarnings("unused")
    public String thirdQuestion(String string) {
        return String.valueOf(Pattern.matches("^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", string.strip()));
    }

    /**
     * 4. Написать регулярное выражение, определяющее является ли данная строчка валидным URL адресом.
     * В данной задаче правильным URL считаются адреса http и https, явное указание протокола также может отсутствовать.
     * Учитываются только адреса, состоящие из символов, т.е. IP адреса в качестве URL не присутствуют при проверке.
     * Допускаются поддомены, указание порта доступа через двоеточие, GET запросы с передачей параметров,
     * доступ к подпапкам на домене, допускается наличие якоря через решетку.
     * Однобуквенные домены считаются запрещенными. Запрещены спецсимволы, например «–» в начале и конце имени домена.
     * Запрещен символ «_» и пробел в имени домена.
     * При составлении регулярного выражения ориентируйтесь на список правильных и неправильных выражений заданных ниже.
     * – пример правильных выражений: http://www.example.com, http://example.com.
     * – пример неправильных выражений: Just Text, http://a.com.
     */
    @SuppressWarnings("unused")
    public String fourthQuestion(String string) {
        return String.valueOf(Pattern.matches("^https?://(?:www\\.)?[a-z0-9]{2,}\\.(com|ru)$", string.strip()));
    }

    /**
     * 5. Написать регулярное выражение, определяющее является ли данная строчка шестнадцатиричным идентификатором
     * цвета в HTML. Где #FFFFFF для белого, #000000 для черного, #FF0000 для красного и т.д.
     * – пример правильных выражений: #FFFFFF, #FF3421, #00ff00.
     * – пример неправильных выражений: 232323, f#fddee, #fd2.
     */
    @SuppressWarnings("unused")
    public String fifthQuestion(String string) {
        return String.valueOf(Pattern.matches("^#[0-9a-fA-F]{6}$", string.strip()));
    }

    /**
     * 6. Написать регулярное выражение, определяющее является ли данная строчка датой в формате dd/mm/yyyy.
     * Начиная с 1600 года до 9999 года.
     * – пример правильных выражений: 29/02/2000, 30/04/2003, 01/01/2003.
     * – пример неправильных выражений: 29/02/2001, 30-04-2003, 1/1/1899.
     */
    @SuppressWarnings("unused")
    public String sixthQuestion(String string) {
        return String.valueOf(Pattern.matches("^(0[1-9]|1\\d|2[0-8])/(0[1-9]|1[0-2])/((?:1[6-9]|[2-9]\\d)?\\d{2})$" +
                        "|^29/02/(?:(?:1[6-9]|[2-9]\\d)(?:0[48]|[2468][048]|[13579][26])|(?:16|[2468][048]|[3579][26])00)$",
                string.strip()));
    }

    /**
     * 7. Написать регулярное выражение, определяющее является ли данная строчка валидным E-mail адресом согласно RFC
     * под номером 2822.
     * – пример правильных выражений: user@example.com, root@localhost
     * – пример неправильных выражений: bug@@@com.ru, @val.ru, Just Text2.
     */
    @SuppressWarnings("unused")
    public String seventhQuestion(String string) {
        return String.valueOf(Pattern.matches("^\\w+@\\w+(\\.)?\\w+$", string.strip()));
    }

    /**
     * 8. Составить регулярное выражение, определяющее является ли заданная строка IP адресом, записанным в десятичном виде.
     * – пример правильных выражений: 127.0.0.1, 255.255.255.0.
     * – пример неправильных выражений: 1300.6.7.8, abc.def.gha.bcd.
     */
    @SuppressWarnings("unused")
    public String eighthQuestion(String string) {
        var pattern_str = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 9. Проверить, надежно ли составлен пароль. Пароль считается надежным, если он состоит из 8 или более символов.
     * Где символом может быть английская буква, цифра и знак подчеркивания.
     * Пароль должен содержать хотя бы одну заглавную букву, одну маленькую букву и одну цифру.
     * – пример правильных выражений: C00l_Pass, SupperPas1.
     * – пример неправильных выражений: Cool_pass, C00l.
     */
    @SuppressWarnings("unused")
    public String ninthQuestion(String string) {
        var pattern_str = "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)[A-Za-z0-9_]{8,}$";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 10. Проверить является ли заданная строка шестизначным числом, записанным в десятичной системе счисления без
     * нулей в старших разрядах.
     * – пример правильных выражений: 123456, 234567.
     * – пример неправильных выражений: 1234567, 12345.
     */
    @SuppressWarnings("unused")
    public String tenthQuestion(String string) {
        var pattern_str = "^[1-9]\\d{5}$";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 11. Есть текст со списками цен. Извлечь из него цены в USD, RUR, EU.
     * – пример правильных выражений: 23.78 USD.
     * – пример неправильных выражений: 22 UDD, 0.002 USD.
     */
    @SuppressWarnings("unused")
    public String eleventhQuestion(String string) {
        var pattern_str = "(\\d+(?:\\.\\d+)?)\\s+(USD|RUR|EU)";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 12. Проверить существуют ли в тексте цифры, за которыми не стоит «+».
     * – пример правильных выражений: (3 + 5) – 9 × 4.
     * – пример неправильных выражений: 2 * 9 – 6 × 5.
     */
    @SuppressWarnings("unused")
    public String twelfthQuestion(String string) {
        var pattern_str = "\\b\\d+\\s*\\+";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 13. Создать запрос для вывода только правильно написанных выражений со скобками
     * (количество открытых и закрытых скобок должно быть одинаково).
     * – пример правильных выражений: (3 + 5) – 9 × 4.
     * – пример неправильных выражений: ((3 + 5) – 9 × 4.
     */
    @SuppressWarnings("unused")
    public String thirteenthQuestion(String string) {
        Pattern pattern = Pattern.compile("((\\([^()]*\\)[^()]*)*)");
        Matcher matcher = pattern.matcher(string);

        if (!matcher.matches()) {
            return String.valueOf(false);
        }

        int openBrackets = 0;
        int closeBrackets = 0;
        for (char c : string.toCharArray()) {
            if (c == '(') {
                openBrackets++;
            } else if (c == ')') {
                closeBrackets++;
            }
        }

        return String.valueOf(openBrackets == closeBrackets);
    }
}
