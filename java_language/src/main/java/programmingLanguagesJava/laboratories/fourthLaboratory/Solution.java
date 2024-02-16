package programmingLanguagesJava.laboratories.fourthLaboratory;

import programmingLanguagesJava.laboratories.ConsoleReader;
import programmingLanguagesJava.laboratories.fourthLaboratory.classes.Book;
import programmingLanguagesJava.laboratories.fourthLaboratory.classes.ListMerger;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Solution {

    static SingleLinkedList<Integer> list = initialize();
    static DoubleLinkedList<Integer> doubleList = initializeDouble();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Введите номер задания: ");
        var question = scanner.nextInt();

        System.out.printf("---------------------------------------------------\nРезультат %d задания:\n", question);

        Object result = switch (question) {

            case 1, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19,
                    21, 24, 25, 26, 27, 28, 29, 35, 36, 37, 38, 39, 46 ->
                    ConsoleReader.executeTask(Solution.class, String.valueOf(question), " ");

            case 2, 3, 10,
                    22, 23, 30 -> {
                System.out.print("Введите число для задания: ");
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.next());
            }

            case 11, 31 -> {
                System.out.print("Какое вы хотите найти максимальное или минимальное? ");
                scanner.nextLine();
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.nextLine());
            }

            case 12, 13, 32, 33 -> {
                System.out.print("Введите значение для удаления: ");
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.next());
            }

            case 14, 34 -> {
                System.out.print("Введите два значения (старое, новое): ");
                scanner.nextLine();
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.nextLine());
            }

            case 20, 40 -> {
                System.out.println("Как вы хотите сортировать? С помощью указателей или значений? (pointer, data): ");
                scanner.nextLine();
                yield ConsoleReader.executeTask(Solution.class, String.valueOf(question), scanner.nextLine());
            }

            case 41 -> {
                System.out.print("Введите книгу по такому клише (название, автор, год): ");
                // Изучаем Python, Марк Лутц, 2019
                scanner.nextLine();
                yield fortyFirstQuestion(scanner.nextLine());
            }

            case 42 -> {
                System.out.print("Введите два массива. Например, [3, 6, 9] [10, 12, 15]: ");
                scanner.nextLine();
                yield fortySecondQuestion(scanner.nextLine());
            }

            case 43 -> {
                System.out.println("Введите в начале задание, а потом массив. Например: 'положительные числа [3, 2, 1, -15]'");
                scanner.nextLine();
                yield fortyThirdQuestion(scanner.nextLine());
            }

            case 45 -> {
                System.out.print("Введите значения для задания в одной строке через пробел: ");
                scanner.nextLine();
                yield fortyFifthQuestion(scanner.nextLine());
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
        var localList = new SingleLinkedList<>();
        return "Список был инициализирован";
    }

    /**
     * Добавление элемента в начало списка
     */
    @SuppressWarnings("unused")
    public static String secondQuestion(String number) {
        list.addFirst(Integer.valueOf(number.strip()));
        return "Наш связный список после добавления элемента в начало: " + list;
    }

    /**
     * Добавление элемента в конец списка
     */
    @SuppressWarnings("unused")
    public static String thirdQuestion(String number) {
        list.add(Integer.valueOf(number.strip()));
        return "Наш связный список после добавления элемента в конец: " + list;
    }

    /**
     * Показ всех элементов списка
     */
    @SuppressWarnings("unused")
    public static String fourthQuestion(String ignoreUnused) {
        return "Наш связный список: " + list;
    }

    /**
     * Удаление всех элементов списка
     */
    @SuppressWarnings("unused")
    public static String fifthQuestion(String ignoreUnused) {

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
        return String.format("Добавил случайные элементы в связный список: %s\nКоличество элементов: %d", list, list.size());
    }

    /**
     * Проверка списка на пустоту
     */
    @SuppressWarnings("unused")
    public static String seventhQuestion(String ignoreUnused) {
        return String.format("Наш список: %s\nПустота: %s", list, list.isEmpty());
    }

    /**
     * Удаление первого элемента
     */
    @SuppressWarnings("unused")
    public static String eighthQuestion(String ignoreUnused) {
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
        var result = "Наш список: " + list;
        list.delLast();
        result += "\nПосле удаления последнего элемента: " + list;
        return result;

    }

    /**
     * Поиск данного значения в списке
     */
    @SuppressWarnings("unused")
    public static String tenthQuestion(String number) {
        var list = new SingleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(list::add);

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
        var list = new SingleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(list::add);

        var result = "Список до: " + list;
        list.remove((Integer) Integer.parseInt(value));
        result += "\nПосле: " + list;

        return result;
    }

    /**
     * Удаление всех элементов списка с данным значением
     */
    @SuppressWarnings("unused")
    public static String thirteenthQuestion(String string) {
        var list = new SingleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(x -> {
            list.add(x);
            list.add(x);
            list.add(x);
        });

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

        var list = new SingleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(x -> {
            list.add(x);
            list.add(x);
            list.add(x);
        });

        var it = Arrays.stream(args.split("\\s+")).map(Integer::valueOf).iterator();

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

        IntStream.range(1, 11).forEach(symList::add);
        IntStream.iterate(9, i -> i - 1).limit(9).forEach(symList::add);

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

        return String.format("Список: %s\nКоличество разных значений: %d", list, list.countDistinct());
    }

    /**
     * Удаление из списка элементов, значения которых уже встречались в предыдущих элементах.
     */
    @SuppressWarnings("unused")
    public static String eighteenthQuestion(String ignoreUnused) {
        var list = new SingleLinkedList<Integer>();

        var values = Arrays.asList(30, 40, 2, 5, 2, 7, 30, 40, 8);
        values.forEach(list::add);

        return String.format("Список до: %s\nСписок после: %s", list, list.distinct());
    }

    /**
     * Изменение порядка элементов на обратный.
     */
    @SuppressWarnings("unused")
    public static String nineteenthQuestion(String ignoreUnused) {
        var result = "";

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
        var result = "Список: " + list;
        list.sort(param);
        result += "\nСписок после " + param + " сортировки: " + list;
        return result;
    }

    /**
     * Инициализация двусвязного списка
     */
    @SuppressWarnings("unused")
    public static String twentyFirstQuestion(String ignoreUnused) {
        return "Двусвязный список был инициализирован";
    }


    /**
     * Добавление элемента в начало двусвязного списка
     */
    @SuppressWarnings("unused")
    public static String twentySecondQuestion(String number) {
        doubleList.addFirst(Integer.valueOf(number.strip()));
        return "Наш связный список после добавления элемента в начало: " + doubleList;
    }

    /**
     * Добавление элемента в конец двусвязного списка
     */
    @SuppressWarnings("unused")
    public static String twentyThirdQuestion(String number) {
        doubleList.add(Integer.valueOf(number.strip()));
        return "Наш связный список после добавления элемента в конец: " + doubleList;
    }

    /**
     * Показ всех элементов двусвязного списка
     */
    @SuppressWarnings("unused")
    public static String twentyFourthQuestion(String ignoreUnused) {
        return "Наш связный список: " + doubleList;
    }

    /**
     * Удаление всех элементов двусвязного списка
     */
    @SuppressWarnings("unused")
    public static String twentyFifthQuestion(String ignoreUnused) {

        var result = "Добавил случайные элементы в связный список: " + doubleList;
        doubleList.clear();
        result += "\nПосле очистки: " + doubleList;

        return result;
    }

    /**
     * Определение количества элементов двусвязного списка
     */
    @SuppressWarnings("unused")
    public static String twentySixthQuestion(String ignoreUnused) {
        return String.format(
                "Добавил случайные элементы в связный список: %s\nКоличество элементов: %d",
                doubleList,
                doubleList.size()
        );
    }

    /**
     * Проверка двусвязного списка на пустоту
     */
    @SuppressWarnings("unused")
    public static String twentySeventhQuestion(String ignoreUnused) {
        return String.format("Наш список: %s\nПустота: %s", doubleList, doubleList.isEmpty());
    }

    /**
     * Удаление первого элемента двусвязного списка
     */
    @SuppressWarnings("unused")
    public static String twentyEighthQuestion(String ignoreUnused) {
        var result = "Наш список: " + doubleList;
        doubleList.delFirst();
        result += "\nПосле удаления первого элемента: " + doubleList;
        return result;
    }

    /**
     * Удаление последнего элемента двусвязного списка.
     */
    @SuppressWarnings("unused")
    public static String twentyNinthQuestion(String ignoreUnused) {

        var result = "Наш список: " + doubleList;
        doubleList.delLast();
        result += "\nПосле удаления первого элемента: " + doubleList;
        return result;
    }

    /**
     * Поиск данного значения в двусвязном списке
     */
    @SuppressWarnings("unused")
    public static String thirtiethQuestion(String number) {
        var doubleList = new DoubleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(doubleList::add);

        return String.format(
                "Значение %s находится под индексом %d в %s",
                number,
                doubleList.indexOf(Integer.parseInt(number)),
                doubleList
        );
    }

    /**
     * Поиск наибольшего и наименьшего значений в списке
     */
    @SuppressWarnings("unused")
    public static String thirtyFirstQuestion(String argue) {
        return switch (argue.toLowerCase()) {
            case "наибольшее", "максимальное" -> String.format("%d - максимальное значение в %s", doubleList.max(), doubleList);
            case "наименьшее", "минимальное" -> String.format("%d - минимальное значение в %s", doubleList.min(), doubleList);
            default -> "Вы ввели неправильный аргумент к методу";
        };

    }

    /**
     * Удаление элемента двусвязного списка с данным значением
     */
    @SuppressWarnings("unused")
    public static String thirtySecondQuestion(String value) {

        var doubleList = new DoubleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(doubleList::add);

        var result = "Список до: " + doubleList;
        doubleList.remove((Integer) Integer.parseInt(value));
        result += "\nПосле: " + doubleList;

        return result;
    }

    /**
     * Удаление всех элементов списка с данным значением
     */
    @SuppressWarnings("unused")
    public static String thirtyThirdQuestion(String string) {

        var doubleList = new DoubleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(x -> {
            doubleList.add(x);
            doubleList.add(x);
            doubleList.add(x);
        });

        var result = "Список до: " + doubleList;
        doubleList.removeAll(Integer.parseInt(string));
        result += "\nПосле: " + doubleList;

        return result;
    }

    /**
     * Изменение всех элементов списка с данным значением на новое.
     */
    @SuppressWarnings("unused")
    public static String thirtyFourthQuestion(String args) {
        var doubleList = new DoubleLinkedList<Integer>();
        IntStream.range(1, 10).forEach(x -> {
            doubleList.add(x);
            doubleList.add(x);
            doubleList.add(x);
        });

        var it = Arrays.stream(args.split("\\s+")).map(Integer::valueOf).iterator();

        var result = "Список до: " + doubleList;
        doubleList.replace(it.next(), it.next());
        result += "\nПосле: " + doubleList;

        return result;
    }


    /**
     * Определение, является ли список симметричным.
     */
    @SuppressWarnings("unused")
    public static String thirtyFifthQuestion(String ignoreUnused) {
        var symList = new DoubleLinkedList<Integer>();

        IntStream.range(1, 11).forEach(symList::add);
        IntStream.iterate(9, i -> i - 1).limit(9).forEach(symList::add);

        return String.format("Список %s - симметричен (%s)", symList, symList.isSymmetric());
    }

    /**
     * Определение, можно ли удалить из двусвязного списка каких-нибудь два элемента так, чтобы новый список оказался упорядоченным.
     */
    @SuppressWarnings("unused")
    public static String thirtySixthQuestion(String ignoreUnused) {
        var list = new DoubleLinkedList<Integer>();

        var firstTest = Arrays.asList(30, 39, 2, 5, 1, 7, 45, 50, 8);
        var secondTest = Arrays.asList(2, 7, 1, 10, 4);

        secondTest.forEach(list::add);

        return String.format("Список: %s\nМожет быть отсортирован 2 удалениями: %s", list, list.canBeSortedByDeleting2());
    }

    /**
     * Определение, сколько различных значений содержится в двусвязном списке.
     */
    @SuppressWarnings("unused")
    public static String thirtySeventhQuestion(String ignoreUnused) {
        var list = new DoubleLinkedList<Integer>();

        var values = Arrays.asList(30, 40, 2, 5, 2, 7, 30, 40, 8);
        values.forEach(list::add);

        return String.format("Список: %s\nКоличество разных значений: %d", list, list.countDistinct());
    }

    /**
     * Удаление из списка элементов, значения которых уже встречались в предыдущих элементах.
     */
    @SuppressWarnings("unused")
    public static String thirtyEighthQuestion(String ignoreUnused) {
        var list = new DoubleLinkedList<Integer>();

        var values = Arrays.asList(30, 40, 2, 5, 2, 7, 30, 40, 8);
        values.forEach(list::add);

        return String.format("Список: %s\nСписок, содержащий только разные элементы: %s", list, list.distinct());
    }

    /**
     * Изменение порядка элементов на обратный.
     */
    @SuppressWarnings("unused")
    public static String thirtyNinthQuestion(String ignoreUnused) {
        var result = "";

        result += "Список исходный: " + doubleList;
        doubleList.reversed();
        result += "\nРазвернутый список: " + doubleList;
        return result;
    }

    /**
     * Сортировка элементов списка двумя способами (изменение указателей, изменение значений элементов)
     */
    @SuppressWarnings("unused")
    public static String fortiethQuestion(String param) {
        var result = "Список: " + doubleList;
        doubleList.sort(param);
        result += "\nСписок после сортировки вашим способом: " + doubleList;
        return result;
    }

    private static SingleLinkedList<Integer> initialize() {
        var list = new SingleLinkedList<Integer>();
        new Random().ints(10, 5, 1000).forEach(list::add);
        return list;
    }

    private static DoubleLinkedList<Integer> initializeDouble() {
        var list = new DoubleLinkedList<Integer>();
        new Random().ints(10, 5, 1000).forEach(list::add);
        return list;
    }


    /**
     * Дан упорядоченный список книг. Добавить новую книгу, сохранив упорядоченность списка.
     */
    @SuppressWarnings("unused")
    public static String fortyFirstQuestion(String args) {
        var tree = new TreeSet<>(Arrays.asList(
                new Book("Му-му", "Иван Тургенев", 1852),
                new Book("Гарри Поттер", "Джоан Роулинг", 1997)
        ));

        var it = Arrays.stream(args.split(",\\s+")).iterator();

        try {
            var result = "Наш список книг до: " + tree;
            tree.add(new Book(it.next(), it.next(), Integer.parseInt(it.next())));
            result += "\nНаш список книг после: " + tree;
            return result;
        } catch (NoSuchElementException e) {
            return "Ввели неправильные аргументы";
        }

    }

    /**
     * Даны два упорядоченных по возрастанию списка. Объедините их в новый упорядоченный по возрастанию список.
     */
    @SuppressWarnings("unused")
    public static String fortySecondQuestion(String args) {

        try {
            var it = Arrays.stream(args.split("]\\s+\\[")).iterator();
            var firstList = ListMerger.parser(it.next());
            var secondList = ListMerger.parser(it.next());

            return String.format("Результат слияния: %s", ListMerger.mergeSortedLists(firstList, secondList));

        } catch (NoSuchElementException e) {

            return "Вы ввели неправильные данные";
        }

    }

    /**
     * 5. Дан список целых чисел. Упорядочьте по возрастанию только:
     * а) положительные числа;
     * б) элементы с четными порядковыми номерами в списке.
     */
    @SuppressWarnings("unused")
    public static String fortyThirdQuestion(String args) {
        var linkedList = ListMerger.parser(args.substring(args.indexOf("[")));
        Comparator<Integer> comparator;

        if (args.startsWith("положительные числа")) {
            comparator = (o1, o2) -> {
                if (o1 > 0 && o2 > 0)
                    return o1.compareTo(o2);

                if (o1 > 0)
                    return -1;

                if (o2 > 0)
                    return 1;

                return 0;
            };
        }

        else {
            comparator = (o1, o2) -> {
                if (linkedList.indexOf(o1) % 2 == 0 && linkedList.indexOf(o2) % 2 == 0)
                    return o1.compareTo(o2);
                return 0;
            };
        }


        linkedList.sort(comparator);

        return "Результат сортировки: " + linkedList;
    }

    /**
     * Даны два списка. Определите, совпадают ли множества их элементов.
     */
    @SuppressWarnings("unused")
    public static String fortyFourthQuestion(String args) {

        try {

            var it = Arrays.stream(args.split("]\\s+\\[")).iterator();
            var firstList = new HashSet<>(ListMerger.parser(it.next()));
            var secondList = new HashSet<>(ListMerger.parser(it.next()));

            return firstList.equals(secondList) ? "Множества элементов совпадают" : "Множества элементов не совпадают";

        } catch (NoSuchElementException e) {
            return "Вы ввели неправильные данные";
        }

    }

    /**
     * Дан список. После каждого элемента добавьте предшествующую ему часть списка.
     */
    @SuppressWarnings("unused")
    public static String fortyFifthQuestion(String args) {
        var past = new StringBuilder();
        var list = new ArrayList<>(List.of(args.split("\\s+")));

        return list.stream().map(x -> {
            var result = past + x;
            past.append(x);
            return result;
        }).collect(Collectors.joining(" "));
    }

    /**
     * Пусть элементы списка хранят символы предложения. Замените каждое вхождение слова "itmathrepetitor" на "silence".
     */
    @SuppressWarnings("unused")
    public static String fortySixthQuestion(String ignoreUnused) {
        ArrayList<Character> sentenceList = new ArrayList<>(Arrays.asList(
                'i', 't', 'm', 'a', 't', 'h', 'r', 'e', 'p', 'e', 't', 'i', 't', 'o', 'r',
                ' ', ' ', 'p', 'r', 'i', 'v', 'e', 't'
        ));

        var sentence = String.join("", sentenceList.stream().map(Object::toString).toArray(String[]::new));

        return sentence.replaceAll("itmathrepetitor", "silence");
    }

    /**
     * Дан текстовый файл. Создайте двусвязный список, каждый элемент которого содержит количество символов в соответствующей строке текста.
     */
    @SuppressWarnings("unused")
    public static String fortiethSeventhQuestion(String args) {
        return "";
    }

    /**
     * Создайте двусвязный список групп факультета. Каждая группа представляет собой односвязный список студентов.
     */
    @SuppressWarnings("unused")
    public static String fortiethEighthQuestion(String args) {
        return "";
    }

    /**
     * Дан список студентов.
     * Элемент списка содержит фамилию, имя, отчество, год рождения, курс, номер группы, оценки по пяти предметам.
     * Упорядочите студентов по курсу, причем студенты одного курса располагались в алфавитном порядке.
     * Найдите средний балл каждой группы по каждому предмету.
     * Определите самого старшего студента и самого младшего из студентов.
     * Для каждой группы найдите лучшего с точки зрения успеваемости студента.
     */
    @SuppressWarnings("unused")
    public static String fortiethNinthQuestion(String args) {
        return "";
    }

}
