package com.c3equalz.user_service.application.commands.user.delete_user_by_id;

import com.c3equalz.user_service.application.common.ports.EventBus;
import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.errors.user.UserNotFoundByIDError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.errors.AuthorizationError;
import com.c3equalz.user_service.domain.user.events.UserDeletedEvent;
import com.c3equalz.user_service.domain.user.services.AccessService;
import com.c3equalz.user_service.domain.user.services.UserService;
import com.c3equalz.user_service.domain.user.services.authorization.AnyOf;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageSelf;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageSubordinate;
import com.c3equalz.user_service.domain.user.services.authorization.UserManagementContext;
import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

import java.util.List;

/**
 * Handler for deleting a user by ID.
 * <p>
 * - Open to authenticated users.
 * - Deletes users.
 * - Current user can delete himself from system.
 * - Admins can delete subordinate users.
 */
@Slf4j
@RequiredArgsConstructor
public final class DeleteUserByIDCommandHandler {

    private final TransactionManager transactionManager;
    private final UserCommandGateway userCommandGateway;
    private final UserService userService; // Not used in Python example, but kept for consistency
    private final CurrentUserService currentUserService;
    private final EventBus eventBus;
    private final AccessService accessService;

    /**
     * Executes the delete user operation.
     *
     * @param data the command containing the user ID to delete
     * @return Mono that completes when the user is deleted
     * @throws UserNotFoundByIDError if the user is not found
     */
    public Mono<Void> run(DeleteUserByIDCommand data) {
        log.info("Delete user started.");

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

                                User userForDeletion = optionalUser.get();

                                // Authorize: user can manage self or can manage subordinate
                                try {
                                    accessService.authorize(
                                            new AnyOf<>(
                                                    new CanManageSelf(),
                                                    new CanManageSubordinate()
                                            ),
                                            new UserManagementContext(
                                                    currentUser,
                                                    userForDeletion
                                            )
                                    );
                                } catch (AuthorizationError e) {
                                    return Mono.error(e);
                                }

                                // Delete user from database
                                return userCommandGateway.deleteByID(userForDeletion.getId())
                                        .then(eventBus.publish(List.of(new UserDeletedEvent(userForDeletion.getId()))))
                                        .then(transactionManager.commit())
                                        .doOnSuccess(_ -> log.info("User deleted."));
                            });
                });
    }
}
