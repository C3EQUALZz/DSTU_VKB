package org.cequalz;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

@DisplayName("Лабораторная №1 — поиск fault в методе oddOrPos")
class OddOrPosTest {

    @Nested
    @DisplayName("Тест-кейсы, НЕ выполняющие fault (баг скрыт)")
    class FaultNotTriggered {

        @Test
        @DisplayName("Пустой массив — цикл не выполняется, обе версии возвращают 0")
        void emptyArray() {
            int[] x = {};
            assertEquals(0, OddOrPos.oddOrPos(x));
            assertEquals(0, OddOrPos.oddOrPosFixed(x));
        }

        @Test
        @DisplayName("Только неотрицательные значения — ошибка % не проявляется")
        void onlyNonNegative() {
            int[] x = {0, 1, 2, 3, 4, 5};
            // Все нечётные положительные (1, 3, 5) + чётные положительные (2, 4) = 5
            // ноль не считается ни нечётным, ни положительным
            assertEquals(5, OddOrPos.oddOrPos(x));
            assertEquals(5, OddOrPos.oddOrPosFixed(x));
        }

        @Test
        @DisplayName("Все элементы — отрицательные чётные: ни одно условие не срабатывает")
        void allNegativeEven() {
            int[] x = {-2, -4, -6, -8};
            assertEquals(0, OddOrPos.oddOrPos(x));
            assertEquals(0, OddOrPos.oddOrPosFixed(x));
        }

        @Test
        @DisplayName("Все нули — ни одно условие не срабатывает")
        void allZeros() {
            int[] x = {0, 0, 0};
            assertEquals(0, OddOrPos.oddOrPos(x));
            assertEquals(0, OddOrPos.oddOrPosFixed(x));
        }

        @Test
        @DisplayName("Положительные нечётные — второе условие (>0) маскирует ошибку первого")
        void positiveOddMaskedByPositiveCheck() {
            int[] x = {1, 3, 5, 7};
            // Даже если бы x[i] % 2 == 1 не сработало, ветка x[i] > 0 поймала бы их.
            assertEquals(4, OddOrPos.oddOrPos(x));
            assertEquals(4, OddOrPos.oddOrPosFixed(x));
        }
    }

    @Nested
    @DisplayName("Тест-кейсы, выполняющие fault и приводящие к failure")
    class FaultTriggered {

        @Test
        @DisplayName("Один отрицательный нечётный элемент: ожидается 1, баг даёт 0")
        void singleNegativeOdd() {
            int[] x = {-3};

            // Демонстрация бага: в текущем виде метод возвращает 0
            assertEquals(0, OddOrPos.oddOrPos(x),
                    "Fault: (-3) % 2 == -1, поэтому условие == 1 не срабатывает");

            // Исправленный метод считает -3 нечётным
            assertEquals(1, OddOrPos.oddOrPosFixed(x));

            // Версии расходятся ровно на этом входе
            assertNotEquals(OddOrPos.oddOrPos(x), OddOrPos.oddOrPosFixed(x));
        }

        @Test
        @DisplayName("Несколько отрицательных нечётных")
        void multipleNegativeOdd() {
            int[] x = {-1, -3, -5, -7};

            assertEquals(0, OddOrPos.oddOrPos(x));
            assertEquals(4, OddOrPos.oddOrPosFixed(x));
        }

        @Test
        @DisplayName("Смешанный массив: фактический результат «теряет» отрицательные нечётные")
        void mixedArray() {
            int[] x = {-3, -1, 0, 1, 2, 3};
            // Должны посчитаться: -3, -1, 1, 2, 3 → 5
            // Багованный считает только: 1, 2, 3 → 3

            assertEquals(3, OddOrPos.oddOrPos(x));
            assertEquals(5, OddOrPos.oddOrPosFixed(x));
        }

        @Test
        @DisplayName("Граничный случай: Integer.MIN_VALUE+1 (отрицательный нечётный)")
        void integerMinValueOdd() {
            int[] x = {Integer.MIN_VALUE + 1};
            // Integer.MIN_VALUE + 1 == -2147483647 — нечётное число
            assertEquals(0, OddOrPos.oddOrPos(x));
            assertEquals(1, OddOrPos.oddOrPosFixed(x));
        }
    }
}
