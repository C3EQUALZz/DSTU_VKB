package practice_1.question_3;

import lombok.extern.slf4j.Slf4j;
import practice_1.question_2.Deque;

@Slf4j
class DequeStack<T> implements StackOperations<T> {
    private final Deque<T> deque;

    public DequeStack(int size) {
        deque = new Deque<>(size);
    }

    @Override
    public void push(T j) {
        if (isFull()) {
            throw new IllegalStateException("Stack is full. Can't add new element " + j);
        }
        deque.insertRight(j);

        log.debug("Inserted element at right corner = {}, updated deque = {}", j, deque);
    }

    @Override
    public T pop() {
        if (!isEmpty()) {

            var value = deque.removeRight();

            log.debug("Removed element at right corner = {}, updated deque = {}", value, deque);

            return value;
        }
        throw new IllegalStateException("Стек пуст. Невозможно выполнить операцию pop.");
    }

    @Override
    public T peek() {
        if (!isEmpty()) {
            var value = deque.removeRight();
            deque.insertRight(value);

            log.debug("Last element of deque = {}, deque = {}", value, deque);

            return value;
        }
        throw new IllegalStateException("Stack is empty. Can't make peek operation.");
    }

    @Override
    public boolean isEmpty() {
        return deque.isEmpty();
    }

    @Override
    public boolean isFull() {
        return deque.isFull();
    }

    @Override
    public String toString() {
        return deque.toString();
    }
}
