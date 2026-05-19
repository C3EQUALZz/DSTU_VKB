package org.cequalz;

public class OddOrPos {

    /**
     * Count odd or positive elements in an array.
     *
     * Метод из задания №1 — содержит fault.
     * В Java оператор % для отрицательных чисел возвращает отрицательный
     * остаток: (-3) % 2 == -1, поэтому условие x[i] % 2 == 1 не
     * распознаёт отрицательные нечётные числа.
     *
     * @param x array to search
     * @return count of odd or positive elements in x
     */
    public static int oddOrPos(int[] x) {
        int count = 0;
        for (int i = 0; i < x.length; i++) {
            if (x[i] % 2 == 1 || x[i] > 0) {
                count++;
            }
        }
        return count;
    }

    /**
     * Исправленная версия: проверяем «нечётность» через != 0 от остатка,
     * это корректно работает и для отрицательных значений
     * (-3 % 2 == -1, что != 0).
     *
     * @param x array to search
     * @return count of odd or positive elements in x
     */
    public static int oddOrPosFixed(int[] x) {
        int count = 0;
        for (int i = 0; i < x.length; i++) {
            if (x[i] % 2 != 0 || x[i] > 0) {
                count++;
            }
        }
        return count;
    }
}
