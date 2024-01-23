package programmingLanguagesJava.laboratories.fourthLaboratory;

public interface CustomQueue<T> {
    /**
     * Метод добавления элемента в конец списка
     *
     * @param obj элемент, который мы хотим добавить в конец списка
     */
    void add(T obj);

    /**
     * Метод, который удаляет с начала списка.
     *
     * @return возвращает элемент, который удалили с самого начала.
     * <b>Прописан возврат, потому что реализация интерфейса очереди.</b>
     */
    T delFirst();

}
