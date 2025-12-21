package com.c3equalz.user_service.domain.user.services.authorization;

/**
 * Represents a permission that can be evaluated against a context.
 *
 * @param <PC> the type of permission context
 */
public interface Permission<PC extends PermissionContext> {

    /**
     * Checks if this permission is satisfied by the given context.
     *
     * @param context the permission context to evaluate
     * @return true if the permission is satisfied, false otherwise
     */
    boolean isSatisfiedBy(PC context);
}

