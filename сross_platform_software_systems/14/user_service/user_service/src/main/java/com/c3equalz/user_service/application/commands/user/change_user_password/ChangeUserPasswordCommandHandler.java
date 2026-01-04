package com.c3equalz.user_service.application.commands.user.change_user_password;

import com.c3equalz.user_service.application.common.ports.EventBus;
import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.AuthSessionService;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.errors.user.UserNotFoundByIDError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.errors.AuthorizationError;
import com.c3equalz.user_service.domain.user.services.AccessService;
import com.c3equalz.user_service.domain.user.services.UserService;
import com.c3equalz.user_service.domain.user.services.authorization.AnyOf;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageSelf;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageSubordinate;
import com.c3equalz.user_service.domain.user.services.authorization.UserManagementContext;
import com.c3equalz.user_service.domain.user.values.RawPassword;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for changing a user's password by ID.
 * <p>
 * - Open to authenticated users.
 * - Changes password.
 * - Current user can update himself from system.
 * - Admins can update password of subordinate users.
 * - After password change, the current session is invalidated for security.
 */
@Slf4j
@RequiredArgsConstructor
public final class ChangeUserPasswordCommandHandler {

    private final TransactionManager transactionManager;
    private final UserCommandGateway userCommandGateway;
    private final UserService userService;
    private final CurrentUserService currentUserService;
    private final EventBus eventBus;
    private final AccessService accessService;
    private final AuthSessionService authSessionService;

    /**
     * Executes the change user password operation.
     *
     * @param data the command containing the user ID and new password
     * @return Mono that completes when the user password is changed and session is invalidated
     * @throws UserNotFoundByIDError if the user is not found
     */
    public Mono<Void> run(ChangeUserPasswordCommand data) {
        log.info("Change user password started.");

        return currentUserService.getCurrentUser()
                .flatMap(currentUser -> {
                    log.info("Read current user identified. User ID: '{}'.", currentUser.getId());

                    // Read user by ID
                    UserID userId = new UserID(data.user_id());
                    return userCommandGateway.readById(userId)
                            .flatMap(optionalUser -> {
                                if (optionalUser.isEmpty()) {
                                    String msg = String.format("Can't find user by ID: %s", data.user_id());
                                    return Mono.error(new UserNotFoundByIDError(msg));
                                }

                                User userForUpdatePassword = optionalUser.get();

                                // Authorize: user can manage self or can manage subordinate
                                try {
                                    accessService.authorize(
                                            new AnyOf<>(
                                                    new CanManageSelf(),
                                                    new CanManageSubordinate()
                                            ),
                                            new UserManagementContext(
                                                    currentUser,
                                                    userForUpdatePassword
                                            )
                                    );
                                } catch (AuthorizationError e) {
                                    return Mono.error(e);
                                }

                                // Validate and create new password
                                RawPassword validatedPassword = new RawPassword(data.password());

                                // Change user password
                                userService.changePassword(userForUpdatePassword, validatedPassword);

                                // Publish events and commit transaction
                                return eventBus.publish(userService.pullEvents())
                                        .then(transactionManager.commit())
                                        .doOnSuccess(_ -> log.info("Log out: user identified. User ID: '{}'.", currentUser.getId()))
                                        .then(authSessionService.invalidateCurrentSession())
                                        .doOnSuccess(_ -> {
                                            log.info("Log out: done. User ID: '{}'.", currentUser.getId());
                                            log.info("Change user password completed.");
                                        });
                            });
                });
    }
}
