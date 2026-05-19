package org.cequalz;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[][] samples = {
                {-3, -1, 0, 1, 2, 3},
                {-5, -3, -1},
                {2, 4, 6},
                {0, 0, 0},
                {}
        };

        System.out.println("Демонстрация fault в методе oddOrPos\n");
        System.out.printf("%-22s | %-10s | %-10s%n", "Массив", "oddOrPos", "fixed");
        System.out.println("-----------------------+------------+----------");
        for (int[] arr : samples) {
            int buggy = OddOrPos.oddOrPos(arr);
            int fixed = OddOrPos.oddOrPosFixed(arr);
            System.out.printf("%-22s | %-10d | %-10d%n",
                    Arrays.toString(arr), buggy, fixed);
        }
    }
}
