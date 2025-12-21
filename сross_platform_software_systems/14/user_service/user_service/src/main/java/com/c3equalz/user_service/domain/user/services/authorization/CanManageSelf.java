package com.c3equalz.user_service.domain.user.services.authorization;

/**
 * Permission that checks if the subject can manage themselves.
 * Satisfied when subject and target are the same user.
 */
public class CanManageSelf implements Permission<UserManagementContext> {

    @Override
    public boolean isSatisfiedBy(UserManagementContext context) {
        return context.getSubject().equals(context.getTarget());
    }
}

