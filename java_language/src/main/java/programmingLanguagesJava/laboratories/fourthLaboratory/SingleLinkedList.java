package programmingLanguagesJava.laboratories.fourthLaboratory;

import org.jetbrains.annotations.NotNull;

import java.util.Iterator;
import java.util.Spliterator;
import java.util.function.Consumer;

public class SingleLinkedList<T extends Comparable<T>> implements CustomList<T>, Iterable<T> {
    private int size;
    private Node<T> head;
    private Node<T> tail;

    /**
     * Мой класс, который реализует структуру данных LinkedList, здесь происходит
     */
    public SingleLinkedList() {
        this.size = 0;
        this.head = this.tail = null;
    }

    @Override
    public void add(T obj) {
        var newNode = new Node<>(obj, null);
        // Если список пуст, тогда нашей головой станет элемент, который мы добавили.
        if (this.size == 0)
            this.head = this.tail = newNode;
        else {
            this.tail.next = newNode;
            this.tail = newNode;
        }

        this.size++;
    }

    @Override
    public void addFirst(T obj) {
        var newNode = new Node<>(obj, null);

        if (this.size == 0)
            this.head = this.tail = newNode;

        else {
            newNode.next = this.head;
            this.head = newNode;
        }

        this.size++;
    }

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
        previousNode.next = new Node<>(obj, previousNode.next);
    }


    @Override
    public int size() {
        return this.size;
    }


    @Override
    public boolean isEmpty() {
        return this.size == 0;
    }


    @Override
    public T delLast() {
        var removed = this.tail;
        this.tail = getNode(this.size - 2);
        this.tail.next = null;
        this.size--;
        return removed.data;
    }


    @Override
    public T delFirst() {
        var firstNode = this.head;
        this.head = firstNode.next;
        firstNode.next = null;
        this.size--;
        return firstNode.data;
    }

    @Override
    public T remove(int index) {

        if (index == 0)
            return delFirst();

        if (index == this.size - 1)
            return delLast();

        var previousNode = getNode(index - 1);
        var currentNode = previousNode.next;
        previousNode.next = currentNode.next;
        return currentNode.data;
    }

    @Override
    public boolean remove(Object obj) {
        int index = indexOf(obj);
        if (index != -1) {
            this.remove(index);
            return true;
        }
        return false;
    }

    @Override
    public int indexOf(Object obj) {

        var node = this.head;
        for (int i = 0; i < size; i++) {

            if (node.data.equals(obj))
                return i;

            node = node.next;
        }

        return -1;
    }

    @Override
    public T max() {
        var biggestNode = this.head;
        var nodeForCycle = this.head;

        for (int i = 0; i < this.size; i++) {

            if (nodeForCycle.compareTo(biggestNode) > 0)
                biggestNode = nodeForCycle;

            nodeForCycle = nodeForCycle.next;
        }

        return biggestNode.data;
    }


    @Override
    public T min() {
        var minimalNode = this.head;
        var nodeForCycle = this.head;

        for (int i = 0; i < this.size; i++) {

            if (nodeForCycle.compareTo(minimalNode) < 0)
                minimalNode = nodeForCycle;

            nodeForCycle = nodeForCycle.next;
        }

        return minimalNode.data;
    }

    @Override
    public boolean removeAll(Object object) {
        Node<T> current = head;
        Node<T> prev = null;

        while (current != null) {
            if (current.data.equals(object)) {

                if (prev == null)
                    this.head = current.next;
                else
                    prev.next = current.next;
            } else prev = current;

            current = current.next;
        }
        return true;
    }

    @Override
    public void replace(T obj) {

    }

    @Override
    public boolean isSymmetric() {
        return this.size % 2 == 0;
    }


    @Override
    public boolean checkSorted() {
        return false;
    }


    @Override
    public int countDistinct() {
        return 0;
    }


    @Override
    public CustomList<T> distinct() {   
        return null;
    }


    @Override
    public void reversed() {
        Node<T> previous = null;
        Node<T> current = this.head;

        if (current == null)
            return;

        while (current != null) {
            var nextElement = current.next;
            current.next = previous;
            previous = current;

            if (current.next == null)
                this.tail = current;

            current = nextElement;
        }

        this.head = previous;
    }


    @Override
    public CustomList<T> sort(String key) {
        return null;
    }

    @Override
    public T get(int index) {
        return getNode(index).data;
    }

    @Override
    public void clear() {
        this.head = this.tail = null;
        this.size = 0;
    }

    @Override
    public String toString() {
        var curr = head;
        StringBuilder str = new StringBuilder();
        while (curr != null) {
            str.append(curr.data).append(" ");
            curr = curr.next;
        }
        return str.toString();
    }

    @Override
    public @NotNull Iterator<T> iterator() {
        return new Iterator<>() {
            private Node<T> node = head;

            @Override
            public boolean hasNext() {
                return node != null;
            }

            @Override
            public T next() {
                T value = node.data;
                node = node.next;
                return value;
            }
        };
    }

    @Override
    public void forEach(Consumer<? super T> action) {
        Iterable.super.forEach(action);
    }

    @Override
    public Spliterator<T> spliterator() {
        return Iterable.super.spliterator();
    }

    private Node<T> getNode(int index) {
        if (index < 0 || index >= size)
            throw new IndexOutOfBoundsException();


        var node = head;

        for (int i = 0; i < index; i++)
            node = node.next;

        return node;
    }

}
