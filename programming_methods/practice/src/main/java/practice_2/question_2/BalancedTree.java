/**
 * Усовершенствуйте программу из п. 8.1, чтобы она создавала сбалансированное дерево.
 * Одно из возможных решений — проследить за тем, чтобы на нижнем уровне было как можно больше листовых узлов.
 * Для начала создайте трехузловое дерево из каждой пары одноузловых деревьев, с новым корневым узлом +.
 * В результате создается лес трехузловых деревьев. Затем каждая пара трехузловых деревьев объединяется для создания
 * леса семиузловых деревьев.
 * С ростом количества узлов в каждом дереве количество деревьев уменьшается, пока не останется только одно дерево.
 */

package practice_2.question_2;

import practice_2.core.AbstractTree;
import practice_2.core.Node;

import java.util.Collection;
import java.util.LinkedList;
import java.util.stream.Collectors;

public class BalancedTree<T extends Comparable<T>> extends AbstractTree<T> {

    public BalancedTree(Collection<T> input) {
        super(input);
    }

    /**
     * Данный конструктор принимает коллекцию элементов, по которой можно итерироваться и собирает дерево.
     *
     * @param input итерируемая коллекция, где элементы поддерживают сравнение.
     */
    @Override
    @SuppressWarnings("unchecked")
    protected Node<T> buildTree(Collection<T> input) {
        var forest = input.stream().map(Node::new).collect(Collectors.toList());

        while (forest.size() > 1) {
            var newForest = new LinkedList<Node<T>>();
            for (int i = 0; i < forest.size(); i += 2) {
                var leftChild = forest.get(i);
                var rightChild = i + 1 < forest.size() ? forest.get(i + 1) : null;
                var value = (T) Character.valueOf('+');
                newForest.add(new Node<>(value, leftChild, rightChild));
            }
            forest = newForest;
        }

        return forest.getFirst();
    }

}
