package practice_5;

import practice_5.core.AbstractHashTable;
import practice_5.question_1.QuadraticProbingHashTable;
import practice_5.question_2.LinearProbingHashTable;

import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        AbstractHashTable<Integer, String> hashTable;

        while (true) {
            try {
                System.out.print("Введите какой вы хотите словарь. (1) - квадратичное пробирование, (2) - линейное пробирование: ");
                hashTable = switch (scanner.nextLine()) {
                    case "1" -> new QuadraticProbingHashTable<>();
                    case "2" -> new LinearProbingHashTable<>();
                    default -> throw new NumberFormatException();
                };
                break;
            } catch (NumberFormatException e) {
                System.out.println("Неправильный выбрали номер, перезапускаю ");
            }
        }


        while (true) {
            System.out.println("\nЧто вы хотите сделать?");
            System.out.println("1 - Вставить элемент");
            System.out.println("2 - Найти элемент");
            System.out.println("3 - Удалить элемент");
            System.out.println("4 - Посмотреть текущее состояние хеш-таблицы");
            System.out.println("Для выхода введите 'exit'");

            String input = scanner.nextLine().trim();

            if (input.equalsIgnoreCase("exit")) {
                break;
            }

            try {
                switch (input) {

                    case "1" -> {
                        // Вставка элемента
                        System.out.print("Введите ключ (целое число): ");
                        int insertKey = Integer.parseInt(scanner.nextLine().trim());
                        System.out.print("Введите значение (строка): ");
                        String insertValue = scanner.nextLine().trim();
                        hashTable.insert(insertKey, insertValue);
                        System.out.println("Текущая хеш-таблица: " + hashTable);
                    }

                    case "2" -> {
                        // Поиск элемента
                        System.out.print("Введите ключ для поиска: ");
                        int findKey = Integer.parseInt(scanner.nextLine().trim());
                        System.out.println("Есть ли " + findKey + " в словаре? " + hashTable.find(findKey));
                    }

                    case "3" -> {
                        System.out.print("Введите ключ для удаления: ");
                        int deleteKey = Integer.parseInt(scanner.nextLine().trim());
                        hashTable.delete(deleteKey);
                        System.out.println("После удаления " + deleteKey + ": " + hashTable);
                    }

                    case "4" -> System.out.println("Текущая хеш-таблица: " + hashTable);

                    default -> System.out.println("Неверный ввод! Пожалуйста, выберите правильное действие.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Ошибка ввода! Пожалуйста, введите корректные данные.");
            }
        }

        scanner.close();
    }
}
