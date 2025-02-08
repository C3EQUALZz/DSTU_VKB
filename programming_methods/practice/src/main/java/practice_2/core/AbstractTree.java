package practice_2.core;

import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.util.Collection;
import java.util.Stack;

@NoArgsConstructor
@AllArgsConstructor
public abstract class AbstractTree<T extends Comparable<T>> {
    protected Node<T> root;

    public AbstractTree(Collection<T> input) {
        this.root = buildTree(input);
    }

    protected abstract Node<T> buildTree(Collection<T> input);

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

        result.append("......................................................\n");

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
