package com.c3equalz.user_service.application.common.ports;

import com.c3equalz.user_service.domain.user.values.UserID;
import reactor.core.publisher.Mono;

/**
 * Interface for revoking user access.
 */
public interface AccessRevoker {

    /**
     * Removes all access for the specified user.
     * This is typically used when a user cannot be found or is invalid.
     *
     * @param userId the user ID whose access should be revoked
     * @return Mono that completes when access revocation is done
     */
    Mono<Void> removeAllUserAccess(UserID userId);
}
