package practice_2.question_1;

class Node<T extends Comparable<T>> implements Comparable<Node<T>> {
    private T data;
    private Node<T> leftChild;
    private Node<T> rightChild;

    public Node(T data) {
        this(data, null, null);
    }

    public Node(T data, Node<T> leftChild, Node<T> rightChild) {
        this.data = data;
        this.leftChild = leftChild;
        this.rightChild = rightChild;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    public void setLeftChild(Node<T> leftChild) {
        this.leftChild = leftChild;
    }

    public void setRightChild(Node<T> rightChild) {
        this.rightChild = rightChild;
    }

    public Node<T> getLeftChild() {
        return leftChild;
    }

    public Node<T> getRightChild() {
        return rightChild;
    }

    public boolean isLeaf() {
        return leftChild == null && rightChild == null;
    }

    public boolean hasChildren() {
        return leftChild != null || rightChild != null;
    }

    @Override
    public int compareTo(Node<T> other) {
        if (other == null) {
            throw new NullPointerException("Сравниваемый узел не должен быть null.");
        }
        return this.data.compareTo(other.data);
    }

    @Override
    public String toString() {
        return String.valueOf(data);
    }
}
