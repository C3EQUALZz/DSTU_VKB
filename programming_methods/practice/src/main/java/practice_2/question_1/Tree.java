/**
 * Задание №1.
 * Измените программу tree.java (см. листинг 8.1) так, чтобы она создавала двоичное дерево по вводимой пользователем
 * цепочке символов (например, A, B и т. д.).
 * Каждая буква отображается в собственном узле.
 * Дерево должно строиться так, чтобы все узлы, содержащие буквы, были листовыми.
 * Родительские узлы могут содержать какой-нибудь символ, не являющийся буквой, например +.
 * Проследите за тем, чтобы каждый родительский узел имел ровно двух потомков.
 * Неважно, если дерево получится несбалансированным.
 * Обратите внимание: созданное дерево не является деревом поиска;
 * в нем не существует быстрого способа найти заданный узел.
 */


package practice_2.question_1;

import practice_2.core.AbstractTree;
import practice_2.core.Node;

import java.util.Collection;
import java.util.LinkedList;
import java.util.stream.Collectors;

public class Tree<T extends Comparable<T>> extends AbstractTree<T> {

    public Tree(Collection<T> input) {
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

        var newForest = new LinkedList<Node<T>>();

        while (!forest.isEmpty()) {
            var leftChild = newForest.isEmpty() ? forest.removeFirst() : newForest.removeFirst();
            var rightChild = forest.removeFirst();
            var value = (T) Character.valueOf('+');
            newForest.add(new Node<>(value, leftChild, rightChild));
        }

        return newForest.getFirst();
    }
}


