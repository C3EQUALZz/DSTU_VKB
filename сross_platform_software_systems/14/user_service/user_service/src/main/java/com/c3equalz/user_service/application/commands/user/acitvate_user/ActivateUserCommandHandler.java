package com.c3equalz.user_service.application.commands.user.acitvate_user;

import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.errors.user.UserNotFoundByIDError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.services.AccessService;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageRole;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageSubordinate;
import com.c3equalz.user_service.domain.user.services.authorization.RoleManagementContext;
import com.c3equalz.user_service.domain.user.services.authorization.UserManagementContext;
import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for activating a user.
 * <p>
 * - Open to admins.
 * - Restores a previously soft-deleted user.
 * - Only super admins can activate other admins.
 */
@Slf4j
@RequiredArgsConstructor
public final class ActivateUserCommandHandler {

    private final CurrentUserService currentUserService;
    private final UserCommandGateway userCommandGateway;
    private final TransactionManager transactionManager;
    private final AccessService accessService;

    /**
     * Executes the activate user operation.
     *
     * @param data the command containing the user ID to activate
     * @return Mono that completes when the user is activated
     * @throws UserNotFoundByIDError if the user is not found
     */
    public Mono<Void> run(ActivateUserCommand data) {
        log.info("Activate user: started. User ID: '{}'.", data.userID());

        return currentUserService.getCurrentUser()
                .flatMap(currentUser -> {
                    // First authorization check: can manage USER role
                    try {
                        accessService.authorize(
                                new CanManageRole(),
                                new RoleManagementContext(
                                        currentUser,
                                        UserRole.USER
                                )
                        );
                    } catch (com.c3equalz.user_service.domain.user.errors.AuthorizationError e) {
                        return Mono.error(e);
                    }

                    // Read user by ID
                    UserID userId = new UserID(data.userID());
                    return userCommandGateway.readById(userId)
                            .flatMap(optionalUser -> {
                                if (optionalUser.isEmpty()) {
                                    String msg = String.format("Can't find user by ID: %s", data.userID());
                                    return Mono.error(new UserNotFoundByIDError(msg));
                                }

                                User userForActivation = optionalUser.get();

                                // Second authorization check: can manage subordinate
                                try {
                                    accessService.authorize(
                                            new CanManageSubordinate(),
                                            new UserManagementContext(
                                                    currentUser,
                                                    userForActivation
                                            )
                                    );
                                } catch (com.c3equalz.user_service.domain.user.errors.AuthorizationError e) {
                                    return Mono.error(e);
                                }

                                // Toggle user activation to true
                                accessService.toggleUserActivation(userForActivation, true);

                                // Commit transaction
                                return transactionManager.commit()
                                        .doOnSuccess(_ -> log.info(
                                                "Activate user: done. User ID: '{}'.",
                                                userForActivation.getId()
                                        ));
                            });
                });
    }
}
