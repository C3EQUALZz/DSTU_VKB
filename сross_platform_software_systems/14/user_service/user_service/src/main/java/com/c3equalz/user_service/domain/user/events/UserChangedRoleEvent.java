package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.Getter;

/**
 * Event raised when a user's role is changed.
 */
@Getter
public class UserChangedRoleEvent extends BaseDomainEvent {
    private final UserID userId;
    private final UserRole oldRole;
    private final UserRole newRole;

    public UserChangedRoleEvent(UserID userId, UserRole oldRole, UserRole newRole) {
        this.userId = userId;
        this.oldRole = oldRole;
        this.newRole = newRole;
    }
}

