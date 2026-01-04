package com.c3equalz.user_service.application.auth.sign_up;

import com.c3equalz.user_service.application.common.ports.EventBus;
import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.common.views.auth.SignUpView;
import com.c3equalz.user_service.application.constants.AuthConstants;
import com.c3equalz.user_service.application.errors.auth.AlreadyAuthenticatedError;
import com.c3equalz.user_service.application.errors.auth.AuthenticationError;
import com.c3equalz.user_service.application.errors.user.UserAlreadyExistsError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.services.UserService;
import com.c3equalz.user_service.domain.user.values.RawPassword;
import com.c3equalz.user_service.domain.user.values.UserEmail;
import com.c3equalz.user_service.domain.user.values.Username;
import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for user sign up operations.
 * <p>
 * - Open to everyone.
 * - Registers a new user with validation and uniqueness checks.
 * - Passwords are peppered, salted, and stored as hashes.
 * - A logged-in user cannot sign up until the session expires or is terminated.
 */
@Slf4j
@RequiredArgsConstructor
public final class SignUpHandler {

    private final CurrentUserService currentUserService;
    private final UserService userService;
    private final UserCommandGateway userCommandGateway;
    private final TransactionManager transactionManager;
    private final EventBus eventBus;

    /**
     * Executes the sign up operation.
     *
     * @param data the sign up data containing email, name, password, and optional role
     * @return Mono containing the sign up view with user ID
     * @throws AlreadyAuthenticatedError if the user is already authenticated
     * @throws UserAlreadyExistsError if a user with the given email already exists
     */
    public Mono<SignUpView> run(SignUpData data) {
        log.info("Sign up: started. Username: '{}'.", data.name());

        // Check if user is already authenticated
        // If getCurrentUser() succeeds, it means user is authenticated
        return currentUserService.getCurrentUser()
                .flatMap(user -> Mono.<SignUpView>error(new AlreadyAuthenticatedError(AuthConstants.AUTH_ALREADY_AUTHENTICATED)))
                .onErrorResume(AuthenticationError.class, _ -> {
                    // User is not authenticated, continue with sign up process
                    UserEmail email = new UserEmail(data.email());
                    Username name = new Username(data.name());
                    RawPassword rawPassword = new RawPassword(data.password());
                    UserRole role = data.role();

                    // Create user domain entity
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
                                            return new SignUpView(newUser.getId().getValue());
                                        }));
                            });
                });
    }
}
