package programmingLanguagesJava.laboratories.fourthLaboratory;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SingleLinkedListTest {
    private SingleLinkedList<Integer> linkedList;

    @BeforeEach
    void setUp() {
        linkedList = new SingleLinkedList<>();
        for (int i = 0; i < 100; i++) {
            linkedList.add(i);
        }
    }

    /**
     * Когда добавил 100 элементов, тогда размер должен стать 100.
     */
    @Test
    void whenAdded100ElementsThenSizeMustBe100() {
        assertEquals(100, this.linkedList.size());
    }

    /**
     * Когда удалил элемент по индексу, тогда размер должен был уменьшиться.
     */
    @Test
    void whenElementRemovedByIndexThenSizeMustBeDecreased() {
        this.linkedList.remove(5);
        assertEquals(99, this.linkedList.size());
    }

    /**
     * Тест для проверки удаления по значению элемента.
     */
    @Test
    void whenElementRemovedThenSizeMustBeDecreased() {
        this.linkedList.add(5);
        assertEquals(101, linkedList.size());
        // Если будет без приведения к ссылочному типу Integer, то будет удаление по индексу,
        // а не по элементу.
        assertTrue(linkedList.remove((Integer) 5));
        assertEquals(100, linkedList.size());
    }

    /**
     * Когда удалил не существующий элемент, то результат будет false
     */
    @Test
    void whenNonExistentElementRemovedThenReturnFalse() {
        assertFalse(linkedList.remove((Integer) 10000));
        assertEquals(100, linkedList.size());
    }

    /**
     * Когда очистил список, то размер должен быть равен 0.
     */
    @Test
    void whenListClearedThenSizeMustBe0() {
        linkedList.clear();
        assertEquals(0, linkedList.size());
    }

    /**
     * Когда обращаюсь к несуществующему индексу, то бросаю ошибку
     */
    @Test
    void whenIndexOutOfBoundsThenThrownException() throws IndexOutOfBoundsException {
        linkedList.get(100);
    }

    /**
     * Метод должен обращаться правильно к элементу, тут просто тестирую метод get.
     */
    @Test
    void methodGetReturnedRightValue() {
        assertEquals(0, linkedList.get(0));
    }

    /**
     * Метод, который проверяет сортировку.
     */
    @Test
    void checkSort() {
        var ll = new SingleLinkedList<Integer>();
    }
}