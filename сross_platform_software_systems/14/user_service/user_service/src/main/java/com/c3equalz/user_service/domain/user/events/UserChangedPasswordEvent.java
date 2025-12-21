package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.Getter;

/**
 * Event raised when a user changes their password.
 */
@Getter
public class UserChangedPasswordEvent extends BaseDomainEvent {
    private final UserID userId;
    private final String name;
    private final String email;
    private final String role;

    public UserChangedPasswordEvent(UserID userId, String name, String email, String role) {
        this.userId = userId;
        this.name = name;
        this.email = email;
        this.role = role;
    }
}

