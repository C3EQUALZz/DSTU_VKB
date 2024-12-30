package practice_4.question_1;

import lombok.Getter;
import lombok.Setter;
import java.util.*;

@Getter
@Setter
class Node<T extends Comparable<T>> {
    private T value; // Значение вершины
    private boolean wasVisited; // Для проверки посещения (если нужно)
    private Map<Node<T>, Integer> neighbors; // Соседи и веса ребер

    public Node(T value) {
        this.value = value;
        this.wasVisited = false;
        this.neighbors = new HashMap<>();
    }

    /**
     * Связывает текущую вершину с другой с указанным весом
     * @param other другая вершина
     * @param weight вес ребра
     */
    public void connect(Node<T> other, int weight) {
        neighbors.put(other, weight);
    }

    @Override
    public String toString() {
        return String.valueOf(value);
    }
}

