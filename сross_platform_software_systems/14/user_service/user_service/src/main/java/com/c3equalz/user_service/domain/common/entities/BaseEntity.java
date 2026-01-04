package com.c3equalz.user_service.domain.common.entities;

import com.c3equalz.user_service.domain.common.values.BaseValueObject;
import lombok.Getter;
import lombok.Setter;

import java.time.Instant;

/**
 * Base class for domain entities, defined by a unique identity ({@code id}).
 * Subclassing is optional; any implementation honoring this contract is valid.
 * <p>
 * Entities are mutable (except for the {@code id} field), but are compared
 * solely by their {@code id} and type.
 * <p>
 * The {@code id} field is immutable once set and cannot be changed.
 *
 * @param <T> the type of the identity, must extend BaseValueObject
 */
@Getter
@Setter
public abstract class BaseEntity<T extends BaseValueObject> {

    /**
     * Identity that remains constant throughout the entity's lifecycle.
     * This field is final and cannot be modified after construction.
     */
    protected final T id;
    protected Instant createdAt;
    protected Instant updatedAt;

    /**
     * Protected constructor prevents direct instantiation of base class.
     *
     * @param id the identity of this entity, must not be null
     * @throws IllegalArgumentException if id is null
     */
    protected BaseEntity(T id) {
        if (id == null) {
            throw new IllegalArgumentException("Entity id cannot be null");
        }
        this.id = id;
        this.createdAt = Instant.now();
        this.updatedAt = Instant.now();
    }

    /**
     * Two entities are considered equal if they have the same type and the same {@code id},
     * regardless of other attribute values.
     *
     * @param obj the object to compare with
     * @return true if the objects are equal, false otherwise
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        BaseEntity<?> entity = (BaseEntity<?>) obj;
        return id.equals(entity.id);
    }

    /**
     * Generate a hash based on entity type and the immutable {@code id}.
     * This allows entities to be used in hash-based collections and
     * reduces the risk of hash collisions between different entity types.
     *
     * @return the hash code
     */
    @Override
    public int hashCode() {
        return getClass().hashCode() ^ id.hashCode();
    }

    /**
     * Returns string representation of the entity.
     * Shows only the class name and the id.
     *
     * @return string representation
     */
    @Override
    public String toString() {
        return getClass().getSimpleName() + "(id=" + id + ")";
    }
}
