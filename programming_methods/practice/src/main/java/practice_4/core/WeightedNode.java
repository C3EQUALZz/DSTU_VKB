package practice_4.core;

import lombok.Getter;
import lombok.Setter;
import java.util.*;

@Getter
@Setter
public class WeightedNode<T extends Comparable<T>> {
    private T value; // Значение вершины
    private Map<WeightedNode<T>, Integer> neighbors; // Соседи и веса ребер

    public WeightedNode(T value) {
        this.value = value;
        this.neighbors = new HashMap<>();
    }

    /**
     * Связывает текущую вершину с другой с указанным весом
     * @param other другая вершина
     * @param weight вес ребра
     */
    public void connect(WeightedNode<T> other, int weight) {
        neighbors.put(other, weight);
    }

    @Override
    public String toString() {
        return String.valueOf(value);
    }
}

