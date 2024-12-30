package practice_5.core;

import lombok.Data;

@Data
public class Entry<K, V> {
    private final K key;
    private V value;
    private boolean isDeleted;

    public Entry(K key, V value) {
        this.key = key;
        this.value = value;
        this.isDeleted = false;
    }
}
