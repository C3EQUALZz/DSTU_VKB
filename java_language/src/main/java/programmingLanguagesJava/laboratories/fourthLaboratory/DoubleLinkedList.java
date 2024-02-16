package programmingLanguagesJava.laboratories.fourthLaboratory;

public class DoubleLinkedList<T extends Comparable<T>> extends SingleLinkedList<T> implements CustomList<T>, Iterable<T> {

    /**
     * Данный метод добавляет в начало связного списка. Все-таки нужен для реализации интерфейса очереди.
     *
     * @param obj объект, который добавляет в начало списка.
     */
    @Override
    public void addFirst(T obj) {
        var node = new Node<>(null, obj, this.head);
        this.head.previous = node;
        this.head = node;
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
            tail = nodePrevious;
        }

        if (nodePrevious != null) {
            nodePrevious.next = nodeNext;
        } else {
            head = nodeNext;
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
        var removed = this.tail;

        // Получаем предпоследний элемент, делаем сразу его хвостом.
        this.tail = this.tail.previous;

        // Говорим, что у хвоста следующий элемент равен null по требованиям.
        this.tail.next = null;

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
        Node<T> current = head;
        Node<T> prev = null;

        while (current != null) {
            if (current.data.equals(object)) {

                if (prev == null) {
                    this.head = current.next;
                    this.head.previous = null;
                }

                else {
                    prev.next = current.next;
                    prev.next.previous = prev;
                }

            } else prev = current;

            current = current.next;
        }
        return true;
    }


    /**
     * Изменение порядка элементов на обратный.
     */
    @Override
    public void reversed() {
        Node<T> previous = null;
        Node<T> current = this.head;

        if (current == null)
            return;

        while (current != null) {
            var nextElement = current.next;
            current.next = previous;
            current.previous = nextElement;
            previous = current;

            if (current.next == null)
                this.tail = current;

            current = nextElement;
        }

        this.head = previous;
    }

    /**
     * Метод добавления элемента в конец списка
     *
     * @param obj элемент, который мы хотим добавить в конец списка
     */
    @Override
    public void add(T obj) {

        if (size == 0) {
            head = new Node<>(null, obj, null);
            tail = head;

        } else {
            Node<T> secondLast = tail;
            tail = new Node<>(secondLast, obj, null);
            secondLast.next = tail;
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
        var nodeToDelete = this.head;

        this.head = nodeToDelete.next;
        this.head.previous = null;
        return nodeToDelete.data;
    }

}
