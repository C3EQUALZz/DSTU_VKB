package programmingLanguagesJava.laboratories.fourthLaboratory;

public class DoubleLinkedList<T extends Comparable<T>> extends SingleLinkedList<T> implements CustomList<T>, Iterable<T> {

    private Node<T> first;
    private Node<T> last;
    private int size = 0;

    /**
     * Данный метод добавляет в начало связного списка. Все-таки нужен для реализации интерфейса очереди.
     *
     * @param obj объект, который добавляет в начало списка.
     */
    @Override
    public void addFirst(T obj) {
        var node = new Node<>(null, obj, this.first);
        this.first.previous = node;
        this.first = node;
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

        if (index == 0) {
            addFirst(obj);
            return;
        }

        if (index == this.size) {
            add(obj);
            return;
        }

        var previousNode = getNode(index - 1);
        previousNode.next = new Node<>(previousNode, obj, previousNode.next);
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
    public T remove(int index) {
        if (index == 0) {
            return delFirst();
        }

        if (index == this.size - 1) {
            return delLast();
        }

        var node = getNode(index);
        var nodeNext = node.next;
        var nodePrevious = node.previous;

        if (nodeNext != null) {
            nodeNext.previous = nodePrevious;
        } else {
            last = nodePrevious;
        }

        if (nodePrevious != null) {
            nodePrevious.next = nodeNext;
        } else {
            first = nodeNext;
        }

        size--;
        return node.data;
    }

    /**
     * Удаляет элемент с конца списка.
     */
    @Override
    public T delLast() {
        // Нода для удаления
        var removed = this.last;

        // Получаем предпоследний элемент, делаем сразу его хвостом.
        this.last = this.last.previous;

        // Говорим, что у хвоста следующий элемент равен null по требованиям.
        this.last.next = null;

        this.size--;

        return removed.data;
    }

    /**
     * Удаление всех элементов списка с данным значением
     *
     * @param object объект, который полностью хотим удалить из списка.
     * @return возвращает true, если размер коллекции поменялся в течение вызова.
     */
    @Override
    public boolean removeAll(Object object) {
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
     */
    @Override
    public void reversed() {

    }

    /**
     * Сортировка элементов списка двумя способами (изменение указателей, изменение значений элементов)
     *
     * @param key - ключ сортировки (изменение указателей - "changePointer", изменение значение - "changeValue").
     */
    @Override
    public void sort(String key) {

    }

    /**
     * Обращение к элементу списка с помощью индексации.
     *
     * @param index целое число от 0 до size - 1
     * @return возвращает элемент списка
     */
    @Override
    public T get(int index) {
        return getNode(index).data;
    }

    @Override
    public void clear() {
        first = null;
        last = null;
        size = 0;
    }

    /**
     * Метод добавления элемента в конец списка
     *
     * @param obj элемент, который мы хотим добавить в конец списка
     */
    @Override
    public void add(T obj) {

        if (size == 0) {
            first = new Node<>(null, obj, null);
            last = first;

        } else {
            Node<T> secondLast = last;
            last = new Node<>(secondLast, obj, null);
            secondLast.next = last;
        }

        size++;
    }

    /**
     * Метод, который удаляет с начала списка.
     *
     * @return возвращает элемент, который удалили с самого начала.
     * <b>Прописан возврат, потому что реализация интерфейса очереди.</b>
     */
    @Override
    public T delFirst() {
        var nodeToDelete = this.first;

        this.first = nodeToDelete.next;
        this.first.previous = null;
        return nodeToDelete.data;
    }

    private Node<T> getNode(int index) {

        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }

        Node<T> node = first;
        for (int i = 0; i < index; i++) {
            node = node.next;
        }

        return node;
    }
}
