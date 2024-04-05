package programmingLanguagesJava.laboratories.GUI.config.ParserLabs;

import java.util.Comparator;

class LaboratoryComparator implements Comparator<Class<?>> {

    /**
     * Штука, чтобы работала сортировка лабораторных работ
     * @param o1 the first object to be compared.
     * @param o2 the second object to be compared.
     * @return возвращает порядок сравнения работ
     */
    @Override
    public int compare(Class<?> o1, Class<?> o2) {

        // Определяем порядок для каждой строки
        int orderS1 = getOrder(getDir(o1.getName()));
        int orderS2 = getOrder(getDir(o2.getName()));

        // Сравниваем порядок строк
        return Integer.compare(orderS1, orderS2);
    }

    /**
     * Метод для определения порядка для каждой строки
     */
    private static int getOrder(String s) {
        return switch (s) {
            case "zero" -> 0;
            case "first" -> 1;
            case "firstdotfirst" -> 2;
            case "second" -> 3;
            case "third" -> 4;
            case "thirddotfirst" -> 5;
            case "fourth" -> 6;
            default -> Integer.MAX_VALUE; // Обработка случаев, которые не входят в вашу последовательность
        };
    }

    /**
     * Костыль, который позволяет получать название папки
     * @param s полный путь, в зависимости от которого можно было получить имя директории
     * @return возвращает папку
     * Да, можно было с помощью библиотек сделать, но мне уже не хочется переделывать этот костыль,
     * так как он 100% отрабатывает
     */
    private static String getDir(String s) {
        return s.substring(s.indexOf("laboratories") + 13, s.indexOf("Laboratory"));
    }

}
