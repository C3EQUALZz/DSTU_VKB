package practice_3.question_1.normal;


import lombok.Getter;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

class Node<T> {
    @Getter
    private final T value;
    private final Set<Node<T>> neighbors;

    public Node(T value) {
        this.value = value;
        this.neighbors = new HashSet<>();
    }

    public Set<Node<T>> getNeighbors() {
        return Collections.unmodifiableSet(neighbors);
    }

    public void connect(Node<T> node) {
        if (this == node) throw new IllegalArgumentException("Can't connect node to itself");
        this.neighbors.add(node);
        node.neighbors.add(this);
    }

}
