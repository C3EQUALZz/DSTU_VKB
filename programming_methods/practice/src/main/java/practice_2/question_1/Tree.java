/**
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

import java.util.Collection;
import java.util.LinkedList;
import java.util.Stack;
import java.util.stream.Collectors;

class Tree<T extends Comparable<T>> {
    private final Node<T> root;

    /**
     * Данный конструктор принимает коллекцию элементов, по которой можно итерироваться и собирает дерево.
     *
     * @param input итерируемая коллекция, где элементы поддерживают сравнение.
     */
    @SuppressWarnings("unchecked")
    public Tree(Collection<T> input) {
        var forest = input.stream().map(Node::new).collect(Collectors.toList());

        var newForest = new LinkedList<Node<T>>();

        while (!forest.isEmpty()) {
            var leftChild = newForest.isEmpty() ? forest.removeFirst() : newForest.removeFirst();
            var rightChild = forest.removeFirst();
            var value = (T) Character.valueOf('+');
            newForest.add(new Node<>(value, leftChild, rightChild));
        }

        root = newForest.getFirst();
    }

    /**
     * Метод для вывода дерева в консоль.
     *
     * @return возвращает строковый вид дерева, как указано в задании.
     */
    @Override
    public String toString() {
        var result = new StringBuilder();
        var globalStack = new Stack<Node<T>>();
        var nBlanks = 32;
        var isRowEmpty = false;

        globalStack.push(root);

        result.append(".....................................\n");

        // Пока в текущем ряду есть элементы для отображения
        while (!isRowEmpty) {
            var localStack = new Stack<Node<T>>();
            isRowEmpty = true;

            result.append(" ".repeat(nBlanks));

            // Обрабатываем текущий уровень
            while (!globalStack.isEmpty()) {
                var node = globalStack.pop();

                if (node != null) {
                    // Добавляем данные текущего узла
                    result.append(node.getData());

                    // Добавляем дочерние элементы в локальный стек
                    localStack.push(node.getLeftChild());
                    localStack.push(node.getRightChild());

                    // Если хотя бы один дочерний элемент есть, ряд не пустой
                    if (node.getLeftChild() != null || node.getRightChild() != null) {
                        isRowEmpty = false;
                    }
                } else {
                    // Если узел пустой, добавляем placeholders
                    result.append("--");
                    localStack.push(null);
                    localStack.push(null);
                }

                result.append(" ".repeat(nBlanks * 2 - 2));
            }

            result.append('\n');
            nBlanks /= 2;

            // Переносим элементы из локального стека обратно в глобальный
            while (!localStack.isEmpty()) {
                globalStack.push(localStack.pop());
            }
        }

        result.append("......................................................\n");

        return result.toString().trim();
    }
}


