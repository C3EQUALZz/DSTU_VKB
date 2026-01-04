package com.c3equalz.user_service.application.commands.user.create_user;

import com.c3equalz.user_service.application.common.ports.EventBus;
import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.common.views.user.CreateUserView;
import com.c3equalz.user_service.application.errors.user.UserAlreadyExistsError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.errors.AuthorizationError;
import com.c3equalz.user_service.domain.user.services.AccessService;
import com.c3equalz.user_service.domain.user.services.UserService;
import com.c3equalz.user_service.domain.user.services.authorization.CanManageRole;
import com.c3equalz.user_service.domain.user.services.authorization.RoleManagementContext;
import com.c3equalz.user_service.domain.user.values.RawPassword;
import com.c3equalz.user_service.domain.user.values.UserEmail;
import com.c3equalz.user_service.domain.user.values.Username;
import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for creating a new user.
 * <p>
 * - Open to authenticated users with appropriate permissions.
 * - Creates a new user with validation and uniqueness checks.
 * - Requires authorization to manage the target role.
 */
@Slf4j
@RequiredArgsConstructor
public final class CreateUserCommandHandler {

    private final TransactionManager transactionManager;
    private final UserCommandGateway userCommandGateway;
    private final UserService userService;
    private final EventBus eventBus;
    private final CurrentUserService currentUserService;
    private final AccessService accessService;

    /**
     * Executes the create user operation.
     *
     * @param data the command containing user data (email, name, password, role)
     * @return Mono containing the create user view with user ID
     * @throws UserAlreadyExistsError if a user with the given email already exists
     */
    public Mono<CreateUserView> run(CreateUserCommand data) {
        log.info("Create user: started. Username: '{}'.", data.name());

        return currentUserService.getCurrentUser()
                .flatMap(currentUser -> {
                    // Authorize: check if current user can manage the target role
                    try {
                        accessService.authorize(
                                new CanManageRole(),
                                new RoleManagementContext(
                                        currentUser,
                                        data.role()
                                )
                        );
                    } catch (AuthorizationError e) {
                        return Mono.error(e);
                    }

                    // Create user domain entity
                    UserEmail email = new UserEmail(data.email());
                    Username name = new Username(data.name());
                    RawPassword rawPassword = new RawPassword(data.password());
                    UserRole role = data.role();

                    User newUser = userService.create(email, name, rawPassword, role);

                    // Check if user with this email already exists
                    return userCommandGateway.readByEmail(newUser.getEmail())
                            .flatMap(optionalUser -> {
                                if (optionalUser.isPresent()) {
                                    String msg = String.format("user with this email: %s already exists", newUser.getEmail().getValue());
                                    return Mono.error(new UserAlreadyExistsError(msg));
                                }

                                // Add user to database
                                return userCommandGateway.add(newUser)
                                        .then(transactionManager.flush())
                                        .then(eventBus.publish(userService.pullEvents()))
                                        .then(transactionManager.commit())
                                        .then(Mono.fromCallable(() -> {
                                            log.info("Create user: done. Username: '{}'.", newUser.getName().getValue());
                                            return new CreateUserView(newUser.getId().getValue());
                                        }));
                            });
                });
    }
}
