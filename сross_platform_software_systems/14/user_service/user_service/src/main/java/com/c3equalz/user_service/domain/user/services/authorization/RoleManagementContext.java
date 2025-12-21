package com.c3equalz.user_service.domain.user.services.authorization;

import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * Context for role management permissions.
 * Contains the subject (user performing the action) and target role (role being assigned).
 */
@Getter
@RequiredArgsConstructor
public class RoleManagementContext extends PermissionContext {
    private final User subject;
    private final UserRole targetRole;
}

