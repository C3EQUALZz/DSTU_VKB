package com.c3equalz.user_service.domain.common;

import lombok.Getter;

import java.lang.reflect.Field;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Base event, from which any domain event should be inherited.
 * Events represent internal operations, which may be executed.
 * <p>
 * Each event has a unique identifier ({@code eventId}) and a timestamp
 * ({@code createdAt}) that are automatically generated when the event is created.
 */
@Getter
public abstract class BaseDomainEvent {

    /**
     * Unique identifier for this event, automatically generated.
     */
    private final UUID eventId;

    /**
     * Timestamp when the event was created, automatically generated.
     */
    private final Instant createdAt;

    /**
     * Protected constructor initializes eventId and createdAt automatically.
     */
    protected BaseDomainEvent() {
        this.eventId = UUID.randomUUID();
        this.createdAt = Instant.now();
    }

    /**
     * Creates a map representation of the event.
     * <p>
     * Excludes specified fields and includes additional fields if provided.
     * Uses reflection to get all non-static, non-synthetic fields.
     *
     * @param exclude set of field names to exclude from the map (can be null)
     * @param include map of additional fields to include (can be null)
     * @return map representation of the event
     */
    public Map<String, Object> toMap(java.util.Set<String> exclude, Map<String, Object> include) {
        Map<String, Object> data = new HashMap<>();
        List<Field> fields = getFields();

        for (Field field : fields) {
            String fieldName = field.getName();
            
            // Skip if field is in exclude set
            if (exclude != null && exclude.contains(fieldName)) {
                continue;
            }

            try {
                field.setAccessible(true);
                Object value = field.get(this);
                data.put(fieldName, value);
            } catch (IllegalAccessException e) {
                // Skip fields that cannot be accessed
            }
        }

        // Add additional fields if provided
        if (include != null) {
            data.putAll(include);
        }

        return data;
    }

    /**
     * Creates a map representation of the event without exclusions or additions.
     *
     * @return map representation of the event
     */
    public Map<String, Object> toMap() {
        return toMap(null, null);
    }

    /**
     * Gets all non-static, non-synthetic fields declared in the class
     * and its superclasses up to BaseDomainEvent.
     *
     * @return list of fields
     */
    private List<Field> getFields() {
        List<Field> fields = new ArrayList<>();
        Class<?> clazz = this.getClass();

        while (clazz != null && clazz != BaseDomainEvent.class && clazz != Object.class) {
            Field[] declaredFields = clazz.getDeclaredFields();
            Arrays.stream(declaredFields)
                    .filter(field -> !java.lang.reflect.Modifier.isStatic(field.getModifiers()))
                    .filter(field -> !field.isSynthetic())
                    .forEach(fields::add);
            clazz = clazz.getSuperclass();
        }

        return fields;
    }
}
