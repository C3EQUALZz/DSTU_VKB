package com.c3equalz.user_service.application.commands.user.change_user_name;

import com.c3equalz.user_service.application.common.ports.EventBus;
import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.errors.user.UserNotFoundByIDError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.services.AccessService;
import com.c3equalz.user_service.domain.user.services.UserService;
import com.c3equalz.user_service.domain.user.services.authorization.AnyOf;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageSelf;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageSubordinate;
import com.c3equalz.user_service.domain.user.services.authorization.UserManagementContext;
import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.domain.user.values.Username;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for changing a user's name by ID.
 * <p>
 * - Open to authenticated users.
 * - Changes username.
 * - Current user can update himself from system.
 * - Admins can update username of subordinate users.
 */
@Slf4j
@RequiredArgsConstructor
public final class ChangeUserNameByIDCommandHandler {

    private final TransactionManager transactionManager;
    private final UserCommandGateway userCommandGateway;
    private final UserService userService;
    private final CurrentUserService currentUserService;
    private final EventBus eventBus;
    private final AccessService accessService;

    /**
     * Executes the change user name operation.
     *
     * @param data the command containing the user ID and new name
     * @return Mono that completes when the user name is changed
     * @throws UserNotFoundByIDError if the user is not found
     */
    public Mono<Void> run(ChangeUserNameByIDCommand data) {
        log.info("Change user name started.");

        return currentUserService.getCurrentUser()
                .flatMap(currentUser -> {
                    log.info("Read current user identified. User ID: '{}'.", currentUser.getId());

                    // Read user by ID
                    UserID userId = new UserID(data.userID());
                    return userCommandGateway.readById(userId)
                            .flatMap(optionalUser -> {
                                if (optionalUser.isEmpty()) {
                                    String msg = String.format("Can't find user by ID: %s", data.userID());
                                    return Mono.error(new UserNotFoundByIDError(msg));
                                }

                                User userForUpdateName = optionalUser.get();

                                // Authorize: user can manage self or can manage subordinate
                                try {
                                    accessService.authorize(
                                            new AnyOf<>(
                                                    new CanManageSelf(),
                                                    new CanManageSubordinate()
                                            ),
                                            new UserManagementContext(
                                                    currentUser,
                                                    userForUpdateName
                                            )
                                    );
                                } catch (com.c3equalz.user_service.domain.user.errors.AuthorizationError e) {
                                    return Mono.error(e);
                                }

                                // Validate and create new username
                                Username validatedName = new Username(data.new_name());

                                // Change username
                                userService.changeName(userForUpdateName, validatedName);

                                // Publish events and commit transaction
                                return eventBus.publish(userService.pullEvents())
                                        .then(transactionManager.commit())
                                        .doOnSuccess(_ -> log.info("Change user name completed."));
                            });
                });
    }
}

