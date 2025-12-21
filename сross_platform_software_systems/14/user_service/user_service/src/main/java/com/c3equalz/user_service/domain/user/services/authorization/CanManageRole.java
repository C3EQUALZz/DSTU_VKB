package com.c3equalz.user_service.domain.user.services.authorization;

import com.c3equalz.user_service.domain.user.values.UserRole;

import java.util.Map;
import java.util.Set;

/**
 * Permission that checks if the subject can manage the target role based on role hierarchy.
 */
public class CanManageRole implements Permission<RoleManagementContext> {

    private final Map<UserRole, Set<UserRole>> roleHierarchy;

    /**
     * Creates a new CanManageRole permission with default role hierarchy.
     */
    public CanManageRole() {
        this(RoleHierarchy.SUBORDINATE_ROLES);
    }

    /**
     * Creates a new CanManageRole permission with custom role hierarchy.
     *
     * @param roleHierarchy the role hierarchy mapping
     */
    public CanManageRole(Map<UserRole, Set<UserRole>> roleHierarchy) {
        this.roleHierarchy = roleHierarchy;
    }

    @Override
    public boolean isSatisfiedBy(RoleManagementContext context) {
        Set<UserRole> allowedRoles = roleHierarchy.getOrDefault(
                context.getSubject().getRole(),
                Set.of()
        );
        return allowedRoles.contains(context.getTargetRole());
    }
}

