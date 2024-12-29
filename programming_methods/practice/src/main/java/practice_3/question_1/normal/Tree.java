package practice_3.question_1.normal;

import lombok.Getter;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Tree<T> {
    @Getter
    private final T value;
    private final List<Tree<T>> children;

    private Tree(T value) {
        this.value = value;
        this.children = new ArrayList<>();
    }

    public static <T> Tree<T> of(T value) {
        return new Tree<>(value);
    }

    public List<Tree<T>> getChildren() {
        return Collections.unmodifiableList(children);
    }

    public Tree<T> addChild(T value) {
        Tree<T> newChild = new Tree<>(value);
        children.add(newChild);
        return newChild;
    }
}