package com.c3equalz.user_service.domain.user.events;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.Getter;

/**
 * Event raised when a user adds a photo.
 */
@Getter
public class UserAddedPhotoEvent extends BaseDomainEvent {
    private final UserID userId;
    private final Object photoId; // Using Object as Image ID type is unknown

    public UserAddedPhotoEvent(UserID userId, Object photoId) {
        this.userId = userId;
        this.photoId = photoId;
    }
}

