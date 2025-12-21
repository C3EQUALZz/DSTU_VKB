package com.c3equalz.user_service.application.auth.logout;

import com.c3equalz.user_service.application.common.services.AuthSessionService;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for user logout operations.
 * <p>
 * - Open to authenticated users.
 * - Logs the user out by deleting the JWT access token from cookies
 * and removing the session from the database.
 */
@Slf4j
@RequiredArgsConstructor
public final class LogOutHandler {

    private final CurrentUserService currentUserService;
    private final AuthSessionService authSessionService;

    /**
     * Executes the logout operation.
     *
     * @return Mono that completes when logout is successful
     * @throws com.c3equalz.user_service.application.errors.AuthenticationError if authentication fails
     * @throws com.c3equalz.user_service.infrastructure.errors.RepoError if repository operation fails
     * @throws com.c3equalz.user_service.domain.user.errors.AuthorizationError if authorization fails
     */
    public Mono<Void> run() {
        log.info("Log out: started for unknown user.");

        return currentUserService.getCurrentUser()
                .flatMap(currentUser -> {
                    log.info("Log out: user identified. User ID: '{}'.", currentUser.getId());
                    return authSessionService.invalidateCurrentSession()
                            .doOnSuccess(v -> log.info("Log out: done. User ID: '{}'.", currentUser.getId()));
                });
    }
}
