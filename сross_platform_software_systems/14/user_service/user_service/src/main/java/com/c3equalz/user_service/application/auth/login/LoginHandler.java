package com.c3equalz.user_service.application.auth.login;

import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.application.common.services.AuthSessionService;
import com.c3equalz.user_service.application.common.services.CurrentUserService;
import com.c3equalz.user_service.application.constants.AuthConstants;
import com.c3equalz.user_service.application.errors.AlreadyAuthenticatedError;
import com.c3equalz.user_service.application.errors.AuthenticationError;
import com.c3equalz.user_service.application.errors.user.UserNotFoundByEmailError;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.services.UserService;
import com.c3equalz.user_service.domain.user.values.RawPassword;
import com.c3equalz.user_service.domain.user.values.UserEmail;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

/**
 * Handler for user login operations.
 * <p>
 * - Open to everyone.
 * - Authenticates registered user, sets a JWT access token with a session ID in cookies, and creates a session.
 * - A logged-in user cannot log in again until the session expires or is terminated.
 * - Authentication renews automatically when accessing protected routes before expiration.
 * - If the JWT is invalid, expired, or the session is terminated, the user loses authentication.
 */
@Slf4j
@RequiredArgsConstructor
public class LoginHandler {

    private final CurrentUserService currentUserService;
    private final UserCommandGateway userCommandGateway;
    private final UserService userService;
    private final AuthSessionService authSessionService;

    /**
     * Executes the login operation.
     *
     * @param data the login data containing email and password
     * @return Mono that completes when login is successful
     * @throws AlreadyAuthenticatedError if the user is already authenticated
     * @throws UserNotFoundByEmailError  if the user is not found by email
     * @throws AuthenticationError       if the password is invalid or the account is inactive
     */
    public Mono<Void> run(LoginData data) {
        log.info("Log in: started. Email: '{}'.", data.email());

        // Check if user is already authenticated
        // If getCurrentUser() succeeds, it means user is authenticated
        return currentUserService.getCurrentUser()
                .flatMap(user -> Mono.<Void>error(new AlreadyAuthenticatedError(AuthConstants.AUTH_ALREADY_AUTHENTICATED)))
                .onErrorResume(AuthenticationError.class, error -> {
                    // User is not authenticated, continue with login process
                    UserEmail email = new UserEmail(data.email());
                    RawPassword password = new RawPassword(data.password());

                    return userCommandGateway.readByEmail(email)
                            .flatMap(optionalUser -> {
                                if (optionalUser.isEmpty()) {
                                    String msg = AuthConstants.USER_NOT_FOUND + ": " + email.getValue();
                                    return Mono.error(new UserNotFoundByEmailError(msg));
                                }

                                User user = optionalUser.get();

                                // Validate password
                                if (!userService.isPasswordValid(user, password)) {
                                    return Mono.error(new AuthenticationError(AuthConstants.AUTH_INVALID_PASSWORD));
                                }

                                // Check if account is active
                                if (!user.isActive()) {
                                    return Mono.error(new AuthenticationError(AuthConstants.AUTH_ACCOUNT_INACTIVE));
                                }

                                // Create session
                                return authSessionService.createSession(user.getId())
                                        .doOnSuccess(v -> log.info(
                                                "Log in: done. User, ID: '{}', username '{}', role '{}'.",
                                                user.getId(),
                                                user.getEmail().getValue(),
                                                user.getRole()
                                        ));
                            });
                });
    }
}
