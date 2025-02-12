package practice_5.question_2;

import lombok.extern.slf4j.Slf4j;
import practice_5.core.AbstractHashTable;
import practice_5.core.Entry;

/**
 * Реализация хэш таблица с линейным пробированием
 */
@Slf4j
public class LinearProbingHashTable<K extends Comparable<K>, V> extends AbstractHashTable<K, V> {

    public LinearProbingHashTable() {
        super();
    }


    public void insert(K key, V value) {
        if (loadFactor() >= LOAD_FACTOR_THRESHOLD) {
            resize();
        }

        int index = hash(key);

        log.debug("Index for new key in hash table: {}", index);

        while (table.get(index) != null && !table.get(index).isDeleted()) {
            if (table.get(index).getKey().equals(key)) {
                log.debug("Key {} already exists in hash table", key);
                table.get(index).setValue(value);
                return;
            }
            index = (index + 1) % table.size(); // Линейное пробирование
            log.debug("New index: {}", index);
        }

        table.set(index, new Entry<>(key, value));
        size++;
    }

    /**
     * Проверяем существует ли элемент в таблице
     */
    public boolean find(K key) {
        int index = hash(key);

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                return true;
            }
            index = (index + 1) % table.size(); // Линейное пробирование
        }

        return false;
    }

    /**
     * Получает значение, которое находится под ключом у хэш таблицы
     */
    public V get(K key) {
        int index = hash(key);

        log.debug("Index for element: {}", index);

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                return table.get(index).getValue();
            }
            index = (index + 1) % table.size(); // Линейное пробирование
        }

        return null;
    }

    /**
     * Удаляет элемент из хэш таблицы
     */
    public void delete(K key) {
        int index = hash(key);

        while (table.get(index) != null) {
            if (!table.get(index).isDeleted() && table.get(index).getKey().equals(key)) {
                table.get(index).setDeleted(true);
                size--;

                // Реорганизация таблицы, если слишком много удаленных элементов
                if (size < table.size() / 4) {
                    resize();
                }
                return;
            }
            index = (index + 1) % table.size(); // Линейное пробирование
        }

        log.debug("Array after value was deleted: {}", table);
    }

}
