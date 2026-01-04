package com.c3equalz.user_service.application.commands.user.grant_admin_by_id;

import com.c3equalz.user_service.application.common.ports.EventBus;
import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.errors.user.UserNotFoundByIDError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.errors.AuthorizationError;
import com.c3equalz.user_service.domain.user.services.AccessService;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageRole;
import com.c3equalz.user_service.domain.user.services.authorization.RoleManagementContext;
import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for granting admin rights to a user by ID.
 * <p>
 * - Open to super admins.
 * - Grants admin rights to a specified user.
 * - Super admin rights can not be changed.
 */
@Slf4j
@RequiredArgsConstructor
public final class GrantAdminByIDCommandHandler {

    private final CurrentUserService currentUserService;
    private final UserCommandGateway userCommandGateway;
    private final TransactionManager transactionManager;
    private final AccessService accessService;
    private final EventBus eventBus;

    /**
     * Executes the grant admin operation.
     *
     * @param data the command containing the user ID to grant admin rights to
     * @return Mono that completes when admin rights are granted
     * @throws UserNotFoundByIDError if the user is not found
     */
    public Mono<Void> run(GrantAdminByIDCommand data) {
        log.info("Grant admin: started. User id: '{}'.", data.user_id());

        return currentUserService.getCurrentUser()
                .flatMap(currentUser -> {
                    // First authorization check: can manage ADMIN role
                    try {
                        accessService.authorize(
                                new CanManageRole(),
                                new RoleManagementContext(
                                        currentUser,
                                        UserRole.ADMIN
                                )
                        );
                    } catch (AuthorizationError e) {
                        return Mono.error(e);
                    }

                    // Read user by ID
                    UserID userId = new UserID(data.user_id());
                    return userCommandGateway.readById(userId)
                            .flatMap(optionalUser -> {
                                if (optionalUser.isEmpty()) {
                                    String msg = String.format("Can't find user by ID: %s", data.user_id());
                                    return Mono.error(new UserNotFoundByIDError(msg));
                                }

                                User userForChangingRole = optionalUser.get();

                                // Toggle user admin role to true
                                accessService.toggleUserAdminRole(userForChangingRole, true);

                                // Publish events and commit transaction
                                return eventBus.publish(accessService.pullEvents())
                                        .then(transactionManager.commit())
                                        .doOnSuccess(_ -> log.info("Grant admin: done. ID: '{}'.", userForChangingRole.getId()));
                            });
                });
    }
}
