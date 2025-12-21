package com.c3equalz.user_service.domain.common.values;

import lombok.EqualsAndHashCode;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Base class for immutable value objects (VO) in domain.
 * Subclassing is optional; any implementation honoring this contract is valid.
 * Defined by instance attributes only; these must be immutable.
 * <p>
 * Value objects must have at least one field.
 * All fields should be final to ensure immutability.
 * <p>
 * Repr policy: toString() includes all non-static, non-synthetic fields.
 * To exclude fields from toString(), override toString() in subclass
 * or use @ToString(exclude = "...") annotation from Lombok.
 * <p>
 */
@EqualsAndHashCode
public abstract class BaseValueObject {

    /**
     * Protected constructor prevents direct instantiation of base class.
     */
    protected BaseValueObject() {
        validate();
    }

    /**
     * Hook for additional validation and ensuring invariants.
     * Called automatically after construction.
     * Subclasses should override this method to perform validation.
     */
    protected abstract void validate();

    /**
     * Returns string representation of value object.
     * <p>
     * - With 1 field: outputs the value only.
     * - With 2+ fields: outputs in {@code name=value} format.
     * <p>
     * Uses reflection to get all non-static, non-synthetic fields.
     * To customize, override this method in subclass.
     *
     * @return string representation of the value object
     */
    @Override
    public String toString() {
        List<Field> fields = getFields();
        
        if (fields.isEmpty()) {
            return getClass().getSimpleName() + "(<no fields>)";
        }

        if (fields.size() == 1) {
            Field field = fields.getFirst();
            try {
                field.setAccessible(true);
                Object value = field.get(this);
                return getClass().getSimpleName() + "(" + formatValue(value) + ")";
            } catch (IllegalAccessException e) {
                return getClass().getSimpleName() + "(<access error>)";
            }
        }

        String fieldStrings = fields.stream()
                .map(field -> {
                    try {
                        field.setAccessible(true);
                        Object value = field.get(this);
                        return field.getName() + "=" + formatValue(value);
                    } catch (IllegalAccessException e) {
                        return field.getName() + "=<access error>";
                    }
                })
                .collect(Collectors.joining(", "));

        return getClass().getSimpleName() + "(" + fieldStrings + ")";
    }

    /**
     * Gets all non-static, non-synthetic fields declared in the class
     * and its superclasses up to BaseValueObject.
     *
     * @return list of fields
     */
    private List<Field> getFields() {
        List<Field> fields = new ArrayList<>();
        Class<?> clazz = this.getClass();

        while (clazz != null && clazz != BaseValueObject.class && clazz != Object.class) {
            Field[] declaredFields = clazz.getDeclaredFields();
            Arrays.stream(declaredFields)
                    .filter(field -> !java.lang.reflect.Modifier.isStatic(field.getModifiers()))
                    .filter(field -> !field.isSynthetic())
                    .forEach(fields::add);
            clazz = clazz.getSuperclass();
        }

        return fields;
    }

    /**
     * Formats a value for string representation.
     * Strings are quoted, null is represented as "null".
     *
     * @param value the value to format
     * @return formatted string
     */
    private String formatValue(Object value) {
        if (value == null) {
            return "null";
        }
        if (value instanceof String || value instanceof Character) {
            return "'" + value + "'";
        }
        return value.toString();
    }
}
