package practice_3.question_1.normal;

import java.util.*;

class BreadthFirstSearchAlgorithm {
    public static <T> List<Tree<T>> search(T value, Tree<T> root) {
        Queue<Tree<T>> queue = new ArrayDeque<>();
        List<Tree<T>> visitedNodes = new ArrayList<>();
        queue.add(root);

        while (!queue.isEmpty()) {
            Tree<T> currentNode = queue.remove();
            visitedNodes.add(currentNode);

            if (currentNode.getValue().equals(value)) {
                break;
            } else {
                queue.addAll(currentNode.getChildren());
            }
        }

        return visitedNodes;
    }

    public static <T> List<Node<T>> search(T value, Node<T> start) {
        Queue<Node<T>> queue = new ArrayDeque<>();
        Set<Node<T>> alreadyVisited = new HashSet<>();
        List<Node<T>> visitedNodes = new ArrayList<>();
        queue.add(start);

        while (!queue.isEmpty()) {
            Node<T> currentNode = queue.remove();
            if (alreadyVisited.contains(currentNode)) {
                continue;
            }

            visitedNodes.add(currentNode);
            alreadyVisited.add(currentNode);

            if (currentNode.getValue().equals(value)) {
                break;
            } else {
                queue.addAll(currentNode.getNeighbors());
            }
        }

        return visitedNodes;
    }
}
