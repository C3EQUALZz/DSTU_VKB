package programmingLanguagesJava.laboratories.fourthLaboratory;

import java.util.Collection;

public class SingleLinkedList<T> implements CustomList<T> {
    public SingleLinkedList() {
    }


    /**
     * Метод добавления элемента в конец списка
     *
     * @param obj элемент, который мы хотим добавить в конец списка
     */
    @Override
    public void add(T obj) {

    }

    /**
     * Метод вставки элемента в список.
     * Замечание: не вижу смысла в реализации отдельных методов addFirst, addLast, когда можно пользоваться этим.
     *
     * @param obj   элемент, который мы хотим вставить в список на определенную позицию.
     * @param index индекс, по которому осуществится вставка.
     */
    @Override
    public void add(T obj, int index) {

    }

    /**
     * Определение количества элементов списка
     *
     * @return возвращает количество элементов в списке, целое число
     */
    @Override
    public int size() {
        return 0;
    }

    /**
     * Проверка списка на пустоту
     *
     * @return возвращает true, если список пустой, в ином случае false
     */
    @Override
    public boolean isEmpty() {
        return false;
    }

    /**
     * Метод, который удаляет элемент по индексу.
     * Замечание: не вижу смысла писать отдельные методы для удаления первого и последнего элемента,
     * когда можно просто вписать индекс здесь
     *
     * @param index целое число (от 0 до size - 1).
     * @return возвращает true, если получилось удалить элемент, в ином случае false.
     */
    @Override
    public boolean remove(int index) {
        return false;
    }

    /**
     * Удаление элемента списка с данным значением
     *
     * @param obj элемент, который мы хотим удалить в односвязном списке.
     * @return возвращает true, если получилось удалить элемент, в ином случае false.
     */
    @Override
    public boolean remove(T obj) {
        return false;
    }

    /**
     * Поиск данного значения в списке
     *
     * @param obj элемент, который мы хотим найти в списке
     * @return возвращает индекс элемента, который мы нашли, в ином случае возвращает -1.
     */
    @Override
    public int indexOf(T obj) {
        return 0;
    }

    /**
     * Поиск наибольшего значения в списке
     *
     * @return возвращает максимальный элемент (значение) в списке.
     */
    @Override
    public T max() {
        return null;
    }

    /**
     * Поиск наименьшего значения в списке.
     *
     * @return возвращает минимальный элемент (значение) в списке.
     */
    @Override
    public T min() {
        return null;
    }

    /**
     * Удаление всех элементов списка с данным значением
     *
     * @param collection любая коллекция, в которой находятся элементы для удаления.
     * @return возвращает true, если размер коллекции поменялся в течение вызова.
     */
    @Override
    public boolean removeAll(Collection<? extends T> collection) {
        return false;
    }

    /**
     * Изменение всех элементов списка с данным значением на новое.
     *
     * @param obj элемент из списка, который мы хотим заменить на новое.
     */
    @Override
    public void replace(T obj) {

    }

    /**
     * Определение, является ли список симметричным.
     *
     * @return возвращает true, если длина size % 2 == 0
     */
    @Override
    public boolean isSymmetric() {
        return false;
    }

    /**
     * Определение, можно ли удалить из списка каких-нибудь два элемента так, чтобы новый список оказался упорядоченным.
     *
     * @return определяет возможно ли такое...
     */
    @Override
    public boolean checkSorted() {
        return false;
    }

    /**
     * Определение, сколько различных значений содержится в списке.
     *
     * @return возвращает целое число - количество различных элементов в списке.
     */
    @Override
    public int countDistinct() {
        return 0;
    }

    /**
     * Удаление из списка элементов, значения которых уже встречались в предыдущих элементах.
     *
     * @return возвращает новый список, где нет повторяющихся элементов.
     */
    @Override
    public CustomList<T> distinct() {
        return null;
    }

    /**
     * Изменение порядка элементов на обратный.
     *
     * @return возвращает новый список, который развернули полностью
     */
    @Override
    public CustomList<T> reversed() {
        return null;
    }

    /**
     * Сортировка элементов списка двумя способами (изменение указателей, изменение значений элементов)
     *
     * @param key - ключ сортировки (изменение указателей - "changePointer", изменение значение - "changeValue").
     * @return возвращает отсортированный список.
     */
    @Override
    public CustomList<T> sort(String key) {
        return null;
    }

    /**
     * Обращение к элементу списка с помощью индексации.
     *
     * @param index целое число от 0 до size - 1
     * @return возвращает элемент списка
     */
    @Override
    public T get(int index) {
        return null;
    }

    @Override
    public void clear() {

    }
}
