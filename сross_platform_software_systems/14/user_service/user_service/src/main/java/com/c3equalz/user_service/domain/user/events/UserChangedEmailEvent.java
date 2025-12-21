package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.Getter;

/**
 * Event raised when a user changes their email.
 */
@Getter
public class UserChangedEmailEvent extends BaseDomainEvent {
    private final UserID userId;
    private final String oldEmail;
    private final String newEmail;
    private final String role;
    private final String name;

    public UserChangedEmailEvent(UserID userId, String oldEmail, String newEmail, String role, String name) {
        this.userId = userId;
        this.oldEmail = oldEmail;
        this.newEmail = newEmail;
        this.role = role;
        this.name = name;
    }
}

