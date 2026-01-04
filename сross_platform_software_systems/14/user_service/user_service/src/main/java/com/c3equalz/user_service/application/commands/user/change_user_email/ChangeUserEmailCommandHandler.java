package com.c3equalz.user_service.application.commands.user.change_user_email;

import com.c3equalz.user_service.application.common.ports.EventBus;
import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
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
import com.c3equalz.user_service.domain.user.values.UserEmail;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for changing a user's email by ID.
 * <p>
 * - Open to authenticated users.
 * - Changes user email.
 * - Current user can update himself from system.
 * - Admins can update email of subordinate users.
 */
@Slf4j
@RequiredArgsConstructor
public final class ChangeUserEmailCommandHandler {

    private final TransactionManager transactionManager;
    private final UserCommandGateway userCommandGateway;
    private final UserService userService;
    private final CurrentUserService currentUserService;
    private final EventBus eventBus;
    private final AccessService accessService;

    /**
     * Executes the change user email operation.
     *
     * @param data the command containing the user ID and new email
     * @return Mono that completes when the user email is changed
     * @throws UserNotFoundByIDError if the user is not found
     */
    public Mono<Void> run(ChangeUserEmailCommand data) {
        log.info("Change user email started.");

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

                                User userForUpdateEmail = optionalUser.get();

                                // Authorize: user can manage self or can manage subordinate
                                try {
                                    accessService.authorize(
                                            new AnyOf<>(
                                                    new CanManageSelf(),
                                                    new CanManageSubordinate()
                                            ),
                                            new UserManagementContext(
                                                    currentUser,
                                                    userForUpdateEmail
                                            )
                                    );
                                } catch (AuthorizationError e) {
                                    return Mono.error(e);
                                }

                                // Validate and create new email
                                UserEmail validatedEmail = new UserEmail(data.new_email());

                                // Change user email
                                userService.changeEmail(userForUpdateEmail, validatedEmail);

                                // Publish events and commit transaction
                                return eventBus.publish(userService.pullEvents())
                                        .then(transactionManager.commit())
                                        .doOnSuccess(_ -> log.info("Change user email completed."));
                            });
                });
    }
}
