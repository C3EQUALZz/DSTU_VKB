/**
 * Измените программу hash.java (см. листинг 11.1) так, чтобы в ней использовалось квадратичное пробирование.
 */

package practice_5.question_1;

import practice_5.core.AbstractHashTable;
import practice_5.core.Entry;

import java.util.ArrayList;

/**
 * HashTable implementation with quadratic probing.
 */
public class QuadraticProbingHashTable<K, V> extends AbstractHashTable<K, V> {
    /**
     * Constructor to initialize the hash table.
     */
    public QuadraticProbingHashTable() {
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

        int hash = hash(key);
        int index = hash;
        int step = 1;

        while (table.get(index) != null && !table.get(index).isDeleted()) {
            if (table.get(index).getKey().equals(key)) {
                // Update existing key
                table.get(index).setValue(value);
                return;
            }
            index = (hash + step * step) % table.size();
            step++;
        }

        table.set(index, new Entry<>(key, value));
        size++;
    }

    /**
     * Checks if a key exists in the hash table.
     */
    public boolean find(K key) {
        int hash = hash(key);
        int index = hash;
        int step = 1;

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                return true; // Key found
            }
            index = (hash + step * step) % table.size();
            step++;
        }

        return false; // Key not found
    }

    /**
     * Retrieves a value by its key in the hash table.
     */
    public V get(K key) {
        int hash = hash(key);
        int index = hash;
        int step = 1;

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                return table.get(index).getValue(); // Return the value if key is found
            }
            index = (hash + step * step) % table.size();
            step++;
        }

        return null; // Key not found
    }

    /**
     * Deletes a key-value pair from the hash table.
     */
    public void delete(K key) {
        int hash = hash(key);
        int index = hash;
        int step = 1;

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                table.get(index).setDeleted(true);
                size--;
                return;
            }
            index = (hash + step * step) % table.size();
            step++;
        }
    }


}

