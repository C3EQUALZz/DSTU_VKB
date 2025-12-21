package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.Getter;

/**
 * Event raised when a user changes their name.
 */
@Getter
public class UserChangedNameEvent extends BaseDomainEvent {
    private final UserID userId;
    private final String oldName;
    private final String newName;
    private final String role;
    private final String email;

    public UserChangedNameEvent(UserID userId, String oldName, String newName, String role, String email) {
        this.userId = userId;
        this.oldName = oldName;
        this.newName = newName;
        this.role = role;
        this.email = email;
    }
}

