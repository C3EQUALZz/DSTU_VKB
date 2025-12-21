package com.c3equalz.user_service.domain.user.services.authorization;

import com.c3equalz.user_service.domain.user.values.UserRole;

import java.util.Map;
import java.util.Set;

/**
 * Permission that checks if the subject can manage the target user based on role hierarchy.
 */
public class CanManageSubordinate implements Permission<UserManagementContext> {

    private final Map<UserRole, Set<UserRole>> roleHierarchy;

    /**
     * Creates a new CanManageSubordinate permission with default role hierarchy.
     */
    public CanManageSubordinate() {
        this(RoleHierarchy.SUBORDINATE_ROLES);
    }

    /**
     * Creates a new CanManageSubordinate permission with custom role hierarchy.
     *
     * @param roleHierarchy the role hierarchy mapping
     */
    public CanManageSubordinate(Map<UserRole, Set<UserRole>> roleHierarchy) {
        this.roleHierarchy = roleHierarchy;
    }

    @Override
    public boolean isSatisfiedBy(UserManagementContext context) {
        Set<UserRole> allowedRoles = roleHierarchy.getOrDefault(
                context.getSubject().getRole(),
                Set.of()
        );
        return allowedRoles.contains(context.getTarget().getRole());
    }
}

