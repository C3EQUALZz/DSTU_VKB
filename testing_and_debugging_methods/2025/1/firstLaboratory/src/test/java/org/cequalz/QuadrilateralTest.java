package org.cequalz;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@DisplayName("Лабораторная №1, Задание №2 — Normal Boundary Value Testing метода area")
class QuadrilateralTest {

    /**
     * Normal Boundary Value Testing (NBVT) для двух входных переменных.
     *
     * Для каждой переменной выбирается 5 типичных граничных точек:
     *   min   = 0
     *   min+  = 1
     *   nom   = 50  (типичное «центральное» значение)
     *   max-  = 99
     *   max   = 100
     *
     * Общее число тест-кейсов для n входных переменных = 4n + 1.
     * Для n = 2 это 9 кейсов: одна переменная пробегает все 5 значений,
     * другая зафиксирована на nominal, и наоборот. Центральная точка
     * (nom, nom) общая для обоих «крестов».
     */
    @Nested
    @DisplayName("Normal Boundary Value: 4n+1 = 9 кейсов")
    class NormalBoundaryValue {

        @ParameterizedTest(name = "[{index}] area({0}, {1}) = {2} — {3}")
        @CsvSource({
                // side1 пробегает 5 значений, side2 = nom
                "0,   50, 0,    'side1=min,  side2=nom'",
                "1,   50, 50,   'side1=min+, side2=nom'",
                "50,  50, 2500, 'side1=nom,  side2=nom (центральная точка)'",
                "99,  50, 4950, 'side1=max-, side2=nom'",
                "100, 50, 5000, 'side1=max,  side2=nom'",

                // side2 пробегает 5 значений, side1 = nom
                // центральная точка (50,50) уже учтена выше
                "50,  0,   0,    'side1=nom, side2=min'",
                "50,  1,   50,   'side1=nom, side2=min+'",
                "50,  99,  4950, 'side1=nom, side2=max-'",
                "50,  100, 5000, 'side1=nom, side2=max'"
        })
        void normalBoundaryValueCase(int side1, int side2, int expected, String description) {
            assertEquals(expected, Quadrilateral.area(side1, side2),
                    "NBVT-кейс не прошёл: " + description);
        }
    }

    /**
     * Дополнительная проверка корректности обработки нарушенных пред-условий.
     * К Normal BVT эти кейсы формально не относятся (это уже Robust BVT),
     * но без них контракт метода был бы не закрыт.
     */
    @Nested
    @DisplayName("Дополнительно: нарушение пред-условий (вне Normal BVT)")
    class PreconditionViolations {

        @Test
        @DisplayName("side1 = -1: должно бросать IllegalArgumentException")
        void side1BelowMin() {
            assertThrows(IllegalArgumentException.class,
                    () -> Quadrilateral.area(-1, 50));
        }

        @Test
        @DisplayName("side1 = 101: должно бросать IllegalArgumentException")
        void side1AboveMax() {
            assertThrows(IllegalArgumentException.class,
                    () -> Quadrilateral.area(101, 50));
        }

        @Test
        @DisplayName("side2 = -1: должно бросать IllegalArgumentException")
        void side2BelowMin() {
            assertThrows(IllegalArgumentException.class,
                    () -> Quadrilateral.area(50, -1));
        }

        @Test
        @DisplayName("side2 = 101: должно бросать IllegalArgumentException")
        void side2AboveMax() {
            assertThrows(IllegalArgumentException.class,
                    () -> Quadrilateral.area(50, 101));
        }
    }
}
