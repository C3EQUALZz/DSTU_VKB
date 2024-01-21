package programmingLanguagesJava.laboratories.fourthLaboratory;

/**
 * Класс, который описывает узел LinkedList
 *
 * @param <T> ссылочный тип данных, который передал пользователь.
 */

public class Node<T extends Comparable<T>> implements Comparable<Node<T>> {
    T data;
    Node<T> previous;
    Node<T> next;

    /**
     * Конструктор класса, который создает наш узел. Данный случай нужен для DoubleLinkedList
     *
     * @param data     элемент узла. Например, цифра 5.
     * @param previous ссылка на прошлый узел
     * @param next     ссылка на следующий узел.
     */
    public Node(Node<T> previous, T data, Node<T> next) {
        this.data = data;
        this.previous = previous;
        this.next = next;
    }

    /**
     * Конструктор класса, который создает наш узел. Данный случай нужен для SingleLinkedList.
     *
     * @param data элемент узла. Например, цифра 5.
     * @param next ссылка на следующий узел.
     */
    public Node(T data, Node<T> next) {
        this.data = data;
        this.next = next;
    }

    /**
     * Встроенный метод интерфейса Comparable, чтобы была поддержка сравнения Node
     *
     * @param o the object to be compared.
     * @return возвращает 0, если объекты равны. 1, если объект, от которого вызываем метод больше, а в ином случае - 1
     * <li>Node(-5).compareTo(Node(-5)) => 0; </li>
     * <li>Node(-5).compareTo(Node(15)) => -1; </li>
     * <li>Node(-5).compareTo(Node(-16)) => 1; </li>
     */
    @Override
    public int compareTo(Node<T> o) {
        return this.data.compareTo(o.data);
    }
}
