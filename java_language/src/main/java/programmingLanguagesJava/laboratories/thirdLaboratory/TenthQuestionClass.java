package programmingLanguagesJava.laboratories.thirdLaboratory;

public class TenthQuestionClass {

    /**
     * Напишите метод, который принимает в качестве параметра любую строку, например “I like Java!!!”.
     */
    static String takesString(String string) {
        return "Вы вписали: " + string;
    }

    /**
     * Распечатать последний символ строки. Используем метод String.charAt().
     */
    static String lastIndex(String string) {
        return String.valueOf(string.charAt(string.length() - 1));
    }

    /**
     * Проверить, заканчивается ли ваша строка подстрокой “!!!”. Используем метод String.endsWith().
     */
    static String endsWithExclamationMark(String string) {
        return String.valueOf(string.endsWith("!!!"));
    }

    /**
     * Проверить, начинается ли ваша строка подстрокой “I like”. Используем метод String.startsWith().
     */
    static String startsWithILike(String string) {
        return String.valueOf(string.startsWith("I like"));
    }

    /**
     * Проверить, содержит ли ваша строка подстроку “Java”. Используем метод String.contains().
     */
    static String containsJava(String string) {
        return String.valueOf(string.contains("Java"));
    }

    /**
     * Найти позицию подстроки “Java” в строке “I like Java!!!”.
     */
    static String indexOfILikeJava() {
        return String.valueOf("I like Java!!!".indexOf("Java"));
    }

    /**
     * Заменить все символы “а” на “о”.
     */
    static String replaceAtoO(String string) {
        return string.replaceAll("a", "o").replaceAll("А", "О");
    }

    /**
     * Преобразуйте строку к верхнему регистру.
     */
    static String toUpperCase(String string) {
        return string.toUpperCase();
    }

    /**
     * Преобразуйте строку к нижнему регистру.
     */
    static String toLowerCase(String string) {
        return string.toLowerCase();
    }

    /**
     * Вырезать строку Java c помощью метода String.substring()
     */
    static String cutFromString(String string) {
        var start = string.indexOf("Java");
        return string.substring(0, start) + string.substring(start + 4, string.length() - 1);
    }

}
