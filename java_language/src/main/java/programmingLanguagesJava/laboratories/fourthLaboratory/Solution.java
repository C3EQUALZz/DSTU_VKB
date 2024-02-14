package programmingLanguagesJava.laboratories.fourthLaboratory;

import programmingLanguagesJava.laboratories.ConsoleReader;

import java.util.Arrays;
import java.util.Random;
import java.util.Scanner;
import java.util.stream.IntStream;

public class Solution {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите номер задания: ");
        var question = scanner.nextInt();

        System.out.printf("---------------------------------------------------\nРезультат %d задания:\n", question);

        Object result = switch (question) {

            case 1, 4, 5, 6, 7, 8, 9, 16 ->
                    ConsoleReader.executeTask(Solution.class, String.valueOf(question), " ");

            case 2, 3, 10 -> {
                System.out.println("Введите число для задания: ");
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.nextInt());
            }

            case 11 -> {
                System.out.print("Какое вы хотите найти максимальное или минимальное? ");
                scanner.nextLine();
                yield eleventhQuestion(scanner.nextLine());
            }

            case 20 -> {
                System.out.println("Как вы хотите сортировать? С помощью указателей или значений? ");
                scanner.nextLine();
                yield twentiethQuestion(scanner.nextLine());
            }

            default -> "Вы выбрали неверное задание";
        };

        scanner.close();
        System.out.println(result);

        }

    /**
     * Инициализация списка
     */
    @SuppressWarnings("unused")
    public static String firstQuestion(String ignoreUnused) {
        var list = new SingleLinkedList<>();
        return "Список был инициализирован";
    }

    /**
     * Добавление элемента в начало списка
     */
    @SuppressWarnings("unused")
    public static String secondQuestion(String number) {
        var list = new SingleLinkedList<Integer>();
        list.addFirst(Integer.valueOf(number.strip()));
        return "Наш связный список после добавления элемента в начало: " + list;
    }

    /**
     * Добавление элемента в конец списка
     */
    @SuppressWarnings("unused")
    public static String thirdQuestion(String number) {
        var list = new SingleLinkedList<Integer>();

        list.add(Integer.valueOf(number.strip()));
        return "Наш связный список после добавления элемента в конец: " + list;
    }

    /**
     * Показ всех элементов списка
     */
    @SuppressWarnings("unused")
    public static String fourthQuestion(String ignoreUnused) {
        var list = initialize();
        return "Наш связный список: " + list;
    }

    /**
     * Удаление всех элементов списка
     */
    @SuppressWarnings("unused")
    public static String fifthQuestion(String ignoreUnused) {
        var list = initialize();

        var result = "Добавил случайные элементы в связный список: " + list;
        list.clear();
        result += "\nПосле очистки: " + list;

        return result;
    }

    /**
     * Определение количества элементов списка
     */
    @SuppressWarnings("unused")
    public static String sixthQuestion(String ignoreUnused) {
        var list = initialize();

        return String.format("Добавил случайные элементы в связный список: %s\nКоличество элементов: %d", list, list.size());
    }

    /**
     * Проверка списка на пустоту
     */
    @SuppressWarnings("unused")
    public static String seventhQuestion(String ignoreUnused) {
        var list = initialize();

        return String.format("Наш список: %s\nПустота: %s", list, list.isEmpty());
    }

    /**
     * Удаление первого элемента
     */
    @SuppressWarnings("unused")
    public static String eighthQuestion(String ignoreUnused) {
        var list = initialize();

        var result = "Наш список: " + list;
        list.delFirst();
        result += "\nПосле удаления первого элемента: " + list;
        return result;
    }

    /**
     * Удаление последнего элемента
     */
    @SuppressWarnings("unused")
    public static String ninthQuestion(String ignoreUnused) {
        var list = initialize();

        var result = "Наш список: " + list;
        list.delFirst();
        result += "\nПосле удаления первого элемента: " + list;
        return result;

    }

    /**
     * Поиск данного значения в списке
     */
    @SuppressWarnings("unused")
    public static String tenthQuestion(String number) {
        var list = initialize();
        return String.format(
                "Значение %s находится под индексом %d в %s",
                number,
                list.indexOf(Integer.parseInt(number)),
                list
        );
    }

    /**
     * Поиск наибольшего и наименьшего значений в списке
     */
    @SuppressWarnings("unused")
    public static String eleventhQuestion(String argue) {
        var list = initialize();

        return switch (argue.toLowerCase()) {
            case "наибольшее", "максимальное" -> String.format("%d - максимальное значение в %s", list.max(), list);
            case "наименьшее", "минимальное" -> String.format("%d - минимальное значение в %s", list.min(), list);
            default -> "Вы ввели неправильный аргумент к методу";
        };

    }

    /**
     * Удаление элемента списка с данным значением
     */
    @SuppressWarnings("unused")
    public static String twelfthQuestion(String value) {
        var list = initialize();

        var result = "Список до: " + list;
        list.remove(Integer.parseInt(value));
        result += "\nПосле: " + list;

        return result;
    }

    /**
     * Удаление всех элементов списка с данным значением
     */
    @SuppressWarnings("unused")
    public static String thirteenthQuestion(String string) {
        var list = initialize();
        var result = "Список до: " + list;
        list.removeAll(Integer.parseInt(string));
        result += "\nПосле: " + list;

        return result;

    }

    /**
     * Изменение всех элементов списка с данным значением на новое.
     */
    @SuppressWarnings("unused")
    public static String fourteenthQuestion(String args) {
        var it = Arrays.stream(args.split("\\s+")).map(Integer::valueOf).iterator();
        var list = initialize();

        var result = "Список до: " + list;
        list.replace(it.next(), it.next());
        result += "\nПосле: " + list;

        return result;
    }

    /**
     * Определение, является ли список симметричным.
     */
    @SuppressWarnings("unused")
    public static String fifteenthQuestion(String ignoreUnused) {
        var symList = new SingleLinkedList<Integer>();

        IntStream.range(1, 10).forEach(symList::add);
        IntStream.range(9, 0).forEach(symList::add);

        return String.format("Список %s - симметричен (%s)", symList, symList.isSymmetric());
    }

    /**
     * Определение, можно ли удалить из списка каких-нибудь два элемента так, чтобы новый список оказался упорядоченным.
     */
    @SuppressWarnings("unused")
    public static String sixteenthQuestion(String ignoreUnused) {
        var list = new SingleLinkedList<Integer>();

        var firstTest = Arrays.asList(30, 40, 2, 5, 1, 7, 45, 50, 8);
        var secondTest = Arrays.asList(2, 7, 1, 10, 4);

        secondTest.forEach(list::add);

        return String.format("Список: %s\nМожет быть отсортирован 2 удалениями: %s", list, list.canBeSortedByDeleting2());
    }

    /**
     * Определение, сколько различных значений содержится в списке.
     */
    @SuppressWarnings("unused")
    public static String seventeenthQuestion(String ignoreUnused) {
        var list = new SingleLinkedList<Integer>();

        var values = Arrays.asList(30, 40, 2, 5, 2, 7, 30, 40, 8);
        values.forEach(list::add);

        return String.format("Список: %s\nКоличество разных значений: ", list.countDistinct());
    }

    /**
     * Удаление из списка элементов, значения которых уже встречались в предыдущих элементах.
     */
    @SuppressWarnings("unused")
    public static String eighteenthQuestion(String ignoreUnused) {
        var list = new SingleLinkedList<Integer>();

        var values = Arrays.asList(30, 40, 2, 5, 2, 7, 30, 40, 8);
        values.forEach(list::add);

        return String.format("Список: %s\nКоличество разных значений: ", list.distinct());
    }

    /**
     * Изменение порядка элементов на обратный.
     */
    @SuppressWarnings("unused")
    public static String nineteenthQuestion(String ignoreUnused) {
        var result = "";
        var list = initialize();

        result += "Список исходный: " + list;
        list.reversed();
        result += "\nРазвернутый список: " + list;
        return result;
    }

    /**
     * Сортировка элементов списка двумя способами (изменение указателей, изменение значений элементов)
     */
    @SuppressWarnings("unused")
    public static String twentiethQuestion(String param) {
        var list = initialize();
        var result = "Список: " + list;
        list.sort(param);
        result += "\nСписок после сортировки вашим способом: " + list;
        return result;
    }

    /**
     * Инициализация списка
     */
    @SuppressWarnings("unused")
    public static String twentyFirst(String ignoreUnused) {
        return "";
    }





    private static SingleLinkedList<Integer> initialize() {
        var list = new SingleLinkedList<Integer>();
        new Random().ints(10, 5, 1000).forEach(list::add);
        return list;
    }

}
