package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.Getter;

/**
 * Event raised when a user's activation status is toggled.
 */
@Getter
public class UserToggleActivationEvent extends BaseDomainEvent {
    private final UserID userId;
    private final boolean isActive;

    public UserToggleActivationEvent(UserID userId, boolean isActive) {
        this.userId = userId;
        this.isActive = isActive;
    }
}

