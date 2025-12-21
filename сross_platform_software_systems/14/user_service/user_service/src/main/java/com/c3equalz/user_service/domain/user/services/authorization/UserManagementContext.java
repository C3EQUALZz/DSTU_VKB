package com.c3equalz.user_service.domain.user.services.authorization;

import com.c3equalz.user_service.domain.user.entities.User;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * Context for user management permissions.
 * Contains the subject (user performing the action) and target (user being managed).
 */
@Getter
@RequiredArgsConstructor
public class UserManagementContext extends PermissionContext {
    private final User subject;
    private final User target;
}

