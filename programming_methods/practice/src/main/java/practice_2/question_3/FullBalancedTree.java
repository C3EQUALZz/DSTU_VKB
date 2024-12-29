package practice_2.question_3;

import practice_2.core.AbstractTree;
import practice_2.core.Node;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

public class FullBalancedTree<T extends Comparable<T>> extends AbstractTree<T> {

    public FullBalancedTree(Collection<T> input) {
        super(input);
    }

    @Override
    protected Node<T> buildTree(Collection<T> input) {
        var forest = input.stream().map(Node::new).collect(Collectors.toList());
        return buildTreeRecursive(forest, 0);
    }

    private Node<T> buildTreeRecursive(List<Node<T>> symbols, int index) {
        if (index < symbols.size()) {
            int leftIndex = 2 * index + 1; // вычисление индекса для левого потомка
            int rightIndex = 2 * index + 2; // вычисление индекса для правого потомка

            var value = symbols.get(index).getData();
            var leftChild = buildTreeRecursive(symbols, leftIndex);
            var rightChild = buildTreeRecursive(symbols, rightIndex);

            return new Node<>(value, leftChild, rightChild);
        }
        return null;
    }
}
