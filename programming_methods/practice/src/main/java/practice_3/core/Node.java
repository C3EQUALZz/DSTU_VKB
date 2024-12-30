package practice_3.core;

import lombok.Getter;
import lombok.Setter;
import java.util.*;

@Getter
@Setter
public class Node<T extends Comparable<T>> {
    private T value;
    private boolean wasVisited;
    private List<Node<T>> neighbors; // Список связей

    public Node(T value) {
        this.value = value;
        this.wasVisited = false;
        this.neighbors = new ArrayList<>();
    }

    /**
     * Связывает текущую вершину с другой
     * @param other другая вершина, которую хотим связать с текущей.
     */
    public void connect(Node<T> other) {
        if (!neighbors.contains(other)) {
            neighbors.add(other);
        }
    }

    @Override
    public String toString() {
        return String.valueOf(value);
    }
}
