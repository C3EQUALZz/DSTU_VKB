package practice_5.core;

import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Slf4j
public abstract class AbstractHashTable<K extends Comparable<K>, V> {
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

        log.debug("Initialized array: {}, default capacity: {}", table, DEFAULT_CAPACITY);
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
        int newCapacity = table.size() * 2;
        List<Entry<K, V>> newTable = new ArrayList<>(Collections.nCopies(newCapacity, null));

        for (Entry<K, V> entry : table) {
            if (entry != null && !entry.isDeleted()) {
                int index = hash(entry.getKey(), newCapacity);
                while (newTable.get(index) != null) {
                    index = (index + 1) % newCapacity; // Линейное пробирование
                }
                newTable.set(index, entry);
            }
        }

        table = newTable;
    }

    /**
     * Computes the hash for a given key.
     */
    protected int hash(K key) {
        return Math.abs(key.hashCode() % table.size());
    }

    protected int hash(K key, int size) {
        return Math.abs(key.hashCode() % size);
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
