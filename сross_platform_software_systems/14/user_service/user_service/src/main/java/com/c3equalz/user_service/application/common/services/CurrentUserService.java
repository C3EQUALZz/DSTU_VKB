package com.c3equalz.user_service.application.common.services;

import com.c3equalz.user_service.application.common.ports.AccessRevoker;
import com.c3equalz.user_service.application.common.ports.IdentityProvider;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.errors.AuthorizationError;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Service for retrieving the current authenticated user.
 */
@Slf4j
@RequiredArgsConstructor
public class CurrentUserService {

    private final IdentityProvider identityProvider;
    private final UserCommandGateway userCommandGateway;
    private final AccessRevoker accessRevoker;

    /**
     * Gets the current authenticated user.
     * <p>
     * If the user cannot be found, all access is revoked and an AuthorizationError is thrown.
     *
     * @return Mono containing the current user
     * @throws AuthorizationError if the user cannot be found
     */
    public Mono<User> getCurrentUser() {
        return identityProvider
                .getCurrentUserID()
                .flatMap(userId -> userCommandGateway.readById(userId)
                        .flatMap(optionalUser -> {
                            if (optionalUser.isPresent()) {
                                return Mono.just(optionalUser.get());
                            } else {
                                log.warn("Failed to retrieve current user. Removing all access. ID: {}.", userId);
                                return accessRevoker
                                        .removeAllUserAccess(userId)
                                        .then(Mono.error(new AuthorizationError("Not authorized.")));
                            }
                        })
                );
    }
}
