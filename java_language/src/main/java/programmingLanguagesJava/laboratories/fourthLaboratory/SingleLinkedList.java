package programmingLanguagesJava.laboratories.fourthLaboratory;

import org.jetbrains.annotations.NotNull;

import java.util.*;
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

        // В LinkedList не было ни одного элемента, тогда новая нода - это и хвост, и голова.
        if (this.size == 0)
            this.head = this.tail = newNode;

        else {
            // В ином случае наша новая нода.next = голова (на первую позицию же вставляем), а потом становится головой.
            newNode.next = this.head;
            this.head = newNode;
        }

        this.size++;
    }

    @Override
    public void add(T obj, int index) {
        // Удобное переопределение, так как я написал уже методы для этого.
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
        // Нода для удаления
        var removed = this.tail;

        // Получаем предпоследний элемент, делаем сразу его хвостом.
        this.tail = getNode(this.size - 2);

        // Говорим, что у хвоста следующий элемент равен null по требованиям.
        this.tail.next = null;

        this.size--;

        return removed.data;
    }


    @Override
    public T delFirst() {
        // Получаем самую первую ноду в связном списке
        var firstNode = this.head;

        // Смещаем указатель на голову на 2 элемент в связном списке.
        this.head = firstNode.next;

        // Обнуляем, так сказать, указатель на следующий элемент.
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
    public void replace(T obj, T replaceObj) {

        while (this.indexOf(obj) != -1) {
            var i = this.indexOf(obj);
            this.getNode(i).data = replaceObj;
        }

    }

    @Override
    public boolean isSymmetric() {

        if (head == null) {
            return true; // Пустой список считается симметричным
        }

        Node<T> currentNode = head;
        List<T> elements = new ArrayList<>();

        // Пройти по всему списку и добавить элементы в массив
        while (currentNode != null) {
            elements.add(currentNode.data);
            currentNode = currentNode.next;
        }

        // Сравнить элементы списка с элементами массива, начиная с конца
        currentNode = head;
        for (int i = elements.size() - 1; i >= 0; i--) {
            if (!currentNode.data.equals(elements.get(i))) {
                return false; // Несимметричный элемент
            }
            currentNode = currentNode.next;
        }

        return true; // Все элементы совпали, список симметричен

    }


    @Override
    public boolean checkSorted() {

        Node<T> previous = this.head;
        Node<T> current = this.head.next;

        var flag = true;

        while (current != null) {

            if (previous.compareTo(current) > 0)
                flag = false;

            if (!flag)
                return flag;


            previous = current;
            current = current.next;

        }

        return flag;
    }


    @Override
    public int countDistinct() {

        var hashSet = new HashSet<>();

        for (var node : this) {
            hashSet.add(node);
        }

        return hashSet.size();
    }


    @Override
    public CustomList<T> distinct() {

        var linkedHashSet = new LinkedHashSet<T>();

        for (var node : this) {
            linkedHashSet.add(node);
        }

        var singleLinkedList = new SingleLinkedList<T>();
        linkedHashSet.forEach(singleLinkedList::add);

        return singleLinkedList;

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
    public void sort(String key) {

        if (key.equals("pointer")) {
            pointerSort();
        }

        else dataSort();

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

    private void swap(Node<T> ptr1, Node<T> ptr2) {
        T tmp = ptr2.data;
        ptr2.data = ptr1.data;
        ptr1.data = tmp;
    }


    private void dataSort() {
        boolean swapped;
        Node<T> current;

        if (head == null) {
            return;
        }

        do {
            swapped = false;
            current = head;

            while (current.next != null) {

                if (current.data.compareTo(current.next.data) > 0) {
                    swap(current, current.next);
                    swapped = true;
                }

                current = current.next;

            }

        } while (swapped);

    }

    private void pointerSort() {
        Node<T> dummyNode = new Node<>(null, null);
        Node<T> currentNode = head;

        while (currentNode != null) {
            Node<T> insertCurrentPos = dummyNode.next;
            Node<T> insertPrePos = null;

            while (insertCurrentPos != null) {
                if (insertCurrentPos.data.compareTo(currentNode.data) > 0) {
                    break;
                }

                insertPrePos = insertCurrentPos;
                insertCurrentPos = insertCurrentPos.next;
            }

            if (insertPrePos == null) {
                insertPrePos = dummyNode;
            }

            Node<T> tempNode = currentNode.next;

            currentNode.next = insertPrePos.next;
            insertPrePos.next = currentNode;

            currentNode = tempNode;
        }

        this.head = dummyNode.next;
        var curr = this.head;
        while (curr.next != null) {
            curr = curr.next;
        }
        this.tail = curr;
    }


    public boolean canBeSortedByDeleting2() {
        int n = this.size();
        ArrayList<T> sub = new ArrayList<>();

        sub.add(this.get(0));

        for (int i = 1; i < n; i++) {

            if (this.get(i).compareTo(sub.getLast()) > 0)
                sub.add(this.get(i));


            else {

                var val = this.get(i);
                var index = binarySearch(sub, val);

                if (index != -1) {
                    sub.set(index, val); // Replace the element at the found index with the current element
                }

            }
        }

        return n - sub.size() == 2;
    }

    private int binarySearch(ArrayList<T> subList, T val) {
        int index = -1; // Initialize index to -1
        int l = 0, r = subList.size() - 1; // Initialize left and right pointers for binary search

        // Binary search to find the index where the current element can be placed in the subsequence
        while (l <= r) {
            int mid = (l + r) / 2; // Calculate the middle index

            if (subList.get(mid).compareTo(val) >= 0) {
                index = mid; // Update the index if the middle element is greater or equal to the current element
                r = mid - 1; // Move the right pointer to mid - 1
            } else {
                l = mid + 1; // Move the left pointer to mid + 1
            }
        }

        return index;
    }


}
