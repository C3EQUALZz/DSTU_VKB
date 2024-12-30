package practice_3.core;

import lombok.Getter;
import lombok.Setter;
import java.util.*;

@Getter
@Setter
public class UnweightedNode<T extends Comparable<T>> {
    private T value;
    private List<UnweightedNode<T>> neighbors; // Список связей

    public UnweightedNode(T value) {
        this.value = value;
        this.neighbors = new ArrayList<>();
    }

    /**
     * Связывает текущую вершину с другой
     * @param other другая вершина, которую хотим связать с текущей.
     */
    public void connect(UnweightedNode<T> other) {
        if (!neighbors.contains(other)) {
            neighbors.add(other);
        }
    }

    @Override
    public String toString() {
        return String.valueOf(value);
    }
}
