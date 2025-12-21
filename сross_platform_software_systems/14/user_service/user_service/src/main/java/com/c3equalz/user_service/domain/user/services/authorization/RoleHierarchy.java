package com.c3equalz.user_service.domain.user.services.authorization;

import com.c3equalz.user_service.domain.user.values.UserRole;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Role hierarchy constants for authorization.
 */
public final class RoleHierarchy {

    /**
     * Mapping of roles to their subordinate roles that can be managed.
     * SUPER_ADMIN can manage ADMIN and USER.
     * ADMIN can manage USER.
     * USER cannot manage anyone.
     */
    public static final Map<UserRole, Set<UserRole>> SUBORDINATE_ROLES = createSubordinateRoles();

    private static Map<UserRole, Set<UserRole>> createSubordinateRoles() {
        Map<UserRole, Set<UserRole>> hierarchy = new HashMap<>();
        hierarchy.put(UserRole.SUPER_ADMIN, Set.of(UserRole.ADMIN, UserRole.USER));
        hierarchy.put(UserRole.ADMIN, Set.of(UserRole.USER));
        hierarchy.put(UserRole.USER, Set.of());
        return Map.copyOf(hierarchy); // Make immutable
    }

    private RoleHierarchy() {
    }
}

