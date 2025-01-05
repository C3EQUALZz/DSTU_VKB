import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class SuperSum {

    public static int[] countPartitions(int[] numbers) {
        Map<Integer, Integer> countMap = new HashMap<>();

        // Подсчитываем количество каждого числа
        for (int number : numbers) {
            countMap.put(number, countMap.getOrDefault(number, 0) + 1);
        }

        int[] results = new int[numbers.length];

        for (int i = 0; i < numbers.length; i++) {
            int number = numbers[i];
            int count = 0;

            for (Map.Entry<Integer, Integer> entry : countMap.entrySet()) {
                int x = entry.getKey();
                int y = number - x;

                if (y < x) {
                    continue; // Избегаем дублирования
                }

                if (x == y) {
                    // Если x и y одинаковые, то выбираем 2 из countMap[x]
                    count += entry.getValue() * (entry.getValue() - 1) / 2;
                } else if (countMap.containsKey(y)) {
                    // Если x и y разные, то просто перемножаем их количества
                    count += entry.getValue() * countMap.get(y);
                }
            }

            results[i] = count;
        }

        return results;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] numbers = new int[n];

        for (int i = 0; i < n; i++) {
            numbers[i] = scanner.nextInt();
        }

        int[] partitions = countPartitions(numbers);

        for (int result : partitions) {
            System.out.println(result);
        }

        scanner.close();
    }
}
