package practice_4.core;

import lombok.AllArgsConstructor;

import java.util.HashMap;
import java.util.Map;

@AllArgsConstructor
public abstract class AbstractWeightedGraph<T extends Comparable<T>> {
    protected final Map<T, WeightedNode<T>> nodes;

    protected AbstractWeightedGraph() {
        this.nodes = new HashMap<>();
    }

    public abstract void addEdge(T from, T to, int weight);


}
