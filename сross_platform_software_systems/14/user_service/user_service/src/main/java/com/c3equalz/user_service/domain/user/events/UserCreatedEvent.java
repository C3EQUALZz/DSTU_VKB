package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.Getter;

/**
 * Event raised when a user is created.
 */
@Getter
public class UserCreatedEvent extends BaseDomainEvent {
    private final UserID userId;
    private final String email;
    private final String name;
    private final UserRole role;

    public UserCreatedEvent(UserID userId, String email, String name, UserRole role) {
        this.userId = userId;
        this.email = email;
        this.name = name;
        this.role = role;
    }
}

