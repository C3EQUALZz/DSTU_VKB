package practice_5.core;

import java.util.ArrayList;
import java.util.List;

public abstract class AbstractHashTable<K, V> {
    protected static final int DEFAULT_CAPACITY = 16;
    protected static final double LOAD_FACTOR_THRESHOLD = 0.75;

    protected List<Entry<K, V>> table;
    protected int size;

    protected AbstractHashTable() {
        table = new ArrayList<>(DEFAULT_CAPACITY);
        for (int i = 0; i < DEFAULT_CAPACITY; i++) {
            table.add(null); // Инициализируем список пустыми элементами
        }
        size = 0;
    }

    public abstract void insert(K key, V value);
    public abstract boolean find(K key);
    public abstract V get(K key);
    public abstract void delete(K key);


    protected double loadFactor() {
        return (double) size / table.size();
    }

    /**
     * Resizes the hash table when the load factor exceeds the threshold.
     */
    protected void resize() {
        List<Entry<K, V>> oldTable = table; // Сохраняем старую таблицу
        table = new ArrayList<>(oldTable.size() * 2); // Создаем новый ArrayList с удвоенной емкостью
        for (int i = 0; i < oldTable.size(); i++) {
            table.add(null); // Инициализируем новый список пустыми элементами
        }

        // Вставляем элементы в новый список
        for (Entry<K, V> entry : oldTable) {
            if (entry != null && !entry.isDeleted()) {
                insert(entry.getKey(), entry.getValue()); // Вставляем элементы в новый список
            }
        }
    }

    /**
     * Computes the hash for a given key.
     */
    protected int hash(K key) {
        return Math.abs(key.hashCode() % table.size());
    }

    /**
     * Returns a string representation of the hash table.
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        for (Entry<K, V> entry : table) {
            if (entry != null && !entry.isDeleted()) {
                sb.append("{").append(entry.getKey()).append("=").append(entry.getValue()).append("}, ");
            }
        }
        if (sb.length() > 11) {
            sb.setLength(sb.length() - 2); // Remove trailing comma and space
        }
        sb.append("]");
        return sb.toString();
    }
}
