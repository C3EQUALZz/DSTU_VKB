package com.c3equalz.user_service.domain.common.entities;

import com.c3equalz.user_service.domain.common.values.BaseValueObject;

/**
 * Base class for aggregate root entities, defined by a unique identity ({@code id}).
 * Subclassing is optional; any implementation honoring this contract is valid.
 * <p>
 * Aggregates are mutable (except for the {@code id} field), but are compared
 * solely by their {@code id} and type.
 * <p>
 * The {@code id} field is immutable once set and cannot be changed.
 *
 * @param <T> the type of the identity, must extend BaseValueObject
 */
public abstract class BaseAggregateRoot<T extends BaseValueObject> extends BaseEntity<T> {
    protected BaseAggregateRoot(T id) {
        super(id);
    }
}
