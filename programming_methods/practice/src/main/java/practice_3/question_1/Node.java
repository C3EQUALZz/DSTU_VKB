package practice_3.question_1;

import lombok.Getter;
import lombok.Setter;
import java.util.*;

@Getter
@Setter
class Node<T extends Comparable<T>> {
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
            other.neighbors.add(this); // Для неориентированного графа
        }
    }

    @Override
    public String toString() {
        return String.valueOf(value);
    }
}
