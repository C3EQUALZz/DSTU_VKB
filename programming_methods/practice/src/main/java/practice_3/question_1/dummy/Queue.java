package practice_3.question_1.dummy;

/**
 * Класс, который описывает очередь. На данный момент смущает его наличие.
 * Ведь в Java есть интерфейс Queue и можно было бы использовать LinkedList
 * Queue q = new LinkedList();
 */
class Queue {
    private final int SIZE = 20;
    private final int[] queArray;
    private int front;
    private int rear;

    // -------------------------------------------------------------
    public Queue() // Конструктор
    {
        queArray = new int[SIZE];
        front = 0;
        rear = -1;
    }

    /**
     * Вставка элемента в конец очереди
     *
     * @param j элемент, который мы хотим вставить.
     */
    public void insert(int j) {
        if (rear == SIZE - 1)
            rear = -1;
        queArray[++rear] = j;
    }

    /**
     * Извлечение элемента в начале очереди
     *
     * @return возвращает элемент, который удалили из начала очереди.
     */
    public int remove() {
        int temp = queArray[front++];
        if (front == SIZE)
            front = 0;
        return temp;
    }

    /**
     * Метод для проверки на пустоту у очереди.
     *
     * @return true, если очередь пуста
     */
    public boolean isEmpty() {
        return (rear + 1 == front || (front + SIZE - 1 == rear));
    }
}
