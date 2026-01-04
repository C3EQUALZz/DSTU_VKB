package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.Getter;

/**
 * Event raised when a user is deleted.
 */
@Getter
public class UserDeletedEvent extends BaseDomainEvent {
    private final UserID userId;

    public UserDeletedEvent(UserID userId) {
        this.userId = userId;
    }
}

