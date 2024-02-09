package programmingLanguagesJava.laboratories.thirdLaboratory;

public class EleventhQuestionClass {
    static String createRows(String firstNumber, String secondNumber) {
        var stringBuilder = new StringBuilder();

        stringBuilder.append(firstNumber + " + " + secondNumber + " = " + (Integer.parseInt(firstNumber) + Integer.parseInt(secondNumber)) + "\n");
        stringBuilder.append(firstNumber + " - " + secondNumber + " = " + (Integer.parseInt(firstNumber) - Integer.parseInt(secondNumber)) + "\n");
        stringBuilder.append(firstNumber + " * " + secondNumber + " = " + (Integer.parseInt(firstNumber) * Integer.parseInt(secondNumber)) + "\n");

        return stringBuilder.toString();
    }

    static String insertDeleteCharAt(String string) {
        var sentence = new StringBuilder(string.strip());

        var equalsPosition = sentence.indexOf("=");

        while (equalsPosition != -1) {
            // Удаление символа '='
            sentence.deleteCharAt(equalsPosition);

            // Вставка слова "равно" вместо удаленного символа
            sentence.insert(equalsPosition, "равно");

            equalsPosition = sentence.indexOf("=");
        }
        return sentence.toString();
    }

    static String replaceStr(String string) {
        return string.replaceAll("=", "равно");
    }

}
