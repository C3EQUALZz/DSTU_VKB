package com.c3equalz.user_service.domain.user.values;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * User role enumeration with string values.
 * Represents different roles that can be assigned to users.
 */
@Getter
@AllArgsConstructor
public enum UserRole {
    SUPER_ADMIN("super_admin"),
    ADMIN("admin"),
    USER("user");

    private final String value;

    /**
     * Checks if this role can be assigned to a user.
     * SUPER_ADMIN role cannot be assigned.
     *
     * @return true if the role is assignable, false otherwise
     */
    public boolean isAssignable() {
        return this != SUPER_ADMIN;
    }

    /**
     * Checks if this role can be changed.
     * SUPER_ADMIN role cannot be changed.
     *
     * @return true if the role is changeable, false otherwise
     */
    public boolean isChangeable() {
        return this != SUPER_ADMIN;
    }

    /**
     * Returns the string value when converted to string.
     * This allows using the enum directly in string contexts.
     *
     * @return the string value of this role
     */
    @Override
    public String toString() {
        return value;
    }
}
