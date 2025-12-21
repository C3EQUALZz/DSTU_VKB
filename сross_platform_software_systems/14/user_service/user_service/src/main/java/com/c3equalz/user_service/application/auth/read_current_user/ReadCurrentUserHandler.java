package com.c3equalz.user_service.application.auth.read_current_user;

import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.common.views.user.ReadUserByIDView;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for reading the current authenticated user.
 * <p>
 * - Opens to everyone.
 * - Get current user, extracting info from cookie.
 */
@Slf4j
@RequiredArgsConstructor
public final class ReadCurrentUserHandler {

    private final CurrentUserService currentUserService;

    /**
     * Executes the read current user operation.
     *
     * @return Mono containing the current user view
     */
    public Mono<ReadUserByIDView> run() {
        log.info("Read current user started.");

        return currentUserService.getCurrentUser()
                .flatMap(currentUser -> {
                    log.info("Read current user identified. User ID: '{}'.", currentUser.getId());

                    ReadUserByIDView view = new ReadUserByIDView(
                            currentUser.getId().getValue(),
                            currentUser.getEmail().getValue(),
                            currentUser.getName().getValue(),
                            currentUser.getRole()
                    );

                    log.info("Read current user ended successfully.");
                    return Mono.just(view);
                });
    }
}
