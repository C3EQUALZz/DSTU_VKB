package practice_5.question_2;

import practice_5.core.AbstractHashTable;
import practice_5.core.Entry;

import java.util.ArrayList;

/**
 * HashTable implementation with linear probing.
 */
public class LinearProbingHashTable<K, V> extends AbstractHashTable<K, V> {
    /**
     * Constructor to initialize the hash table.
     */
    public LinearProbingHashTable() {
        table = new ArrayList<>(DEFAULT_CAPACITY);
        for (int i = 0; i < DEFAULT_CAPACITY; i++) {
            table.add(null); // Инициализируем список пустыми элементами
        }
        size = 0;
    }

    /**
     * Inserts a key-value pair into the hash table.
     */
    public void insert(K key, V value) {
        if (loadFactor() >= LOAD_FACTOR_THRESHOLD) {
            resize();
        }

        int index = hash(key);

        while (table.get(index) != null && !table.get(index).isDeleted()) {
            if (table.get(index).getKey().equals(key)) {
                // Update existing key
                table.get(index).setValue(value);
                return;
            }
            index = (index + 1) % table.size(); // Линейное пробирование
        }

        table.set(index, new Entry<>(key, value));
        size++;
    }

    /**
     * Checks if a key exists in the hash table.
     */
    public boolean find(K key) {
        int index = hash(key);

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                return true; // Key found
            }
            index = (index + 1) % table.size(); // Линейное пробирование
        }

        return false; // Key not found
    }

    /**
     * Retrieves a value by its key in the hash table.
     */
    public V get(K key) {
        int index = hash(key);

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                return table.get(index).getValue(); // Return the value if key is found
            }
            index = (index + 1) % table.size(); // Линейное пробирование
        }

        return null; // Key not found
    }

    /**
     * Deletes a key-value pair from the hash table.
     */
    public void delete(K key) {
        int index = hash(key);

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                table.get(index).setDeleted(true);
                size--;
                return;
            }
            index = (index + 1) % table.size(); // Линейное пробирование
        }
    }

}
