package practice_1.question_3;

class StackX<T> implements StackOperations<T> {
    private final int maxSize;
    private final T[] stackArray;
    private int top;

    @SuppressWarnings("unchecked")
    public StackX(int s) {
        maxSize = s;
        stackArray = (T[]) new Object[maxSize];
        top = -1;
    }

    /**
     * Размещение элемента на вершине стека
     *
     * @param j значение, которое мы хотим разместить на вершине стека.
     */
    @Override
    public void push(T j) {
        stackArray[++top] = j; // Увеличение top, вставка элемента
    }

    /**
     * Извлечение элемента с вершины стека
     *
     * @return элемент, который мы получим с вершины стека
     */
    @Override
    public T pop() {
        return stackArray[top--];
    }

    /**
     * Чтение элемента с вершины стека
     *
     * @return значение с вершины стека.
     */
    @Override
    public T peek() {
        return stackArray[top];
    }

    /**
     * Проверка стека на пустоту.
     *
     * @return возвращает true, если стек пуст, в ином случае false
     */
    @Override
    public boolean isEmpty() {
        return (top == -1);
    }

    /**
     * Проверка заполненности стека.
     *
     * @return True, если стек полон
     */
    @Override
    public boolean isFull() {
        return (top == maxSize - 1);
    }
}
