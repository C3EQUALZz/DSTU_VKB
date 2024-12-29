package practice_2.core;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Node<T extends Comparable<T>> implements Comparable<Node<T>> {
    private T data;
    private Node<T> leftChild;
    private Node<T> rightChild;

    public Node(T data) {
        this(data, null, null);
    }

    @Override
    public int compareTo(Node<T> other) {
        if (other == null) {
            throw new NullPointerException("Сравниваемый узел не должен быть null.");
        }
        return this.data.compareTo(other.data);
    }
}
