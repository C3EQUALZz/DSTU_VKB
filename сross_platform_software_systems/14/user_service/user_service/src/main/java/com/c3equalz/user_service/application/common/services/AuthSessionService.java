package com.c3equalz.user_service.application.common.services;

import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.application.errors.AuthenticationError;
import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.infrastructure.auth.session.AuthSession;
import com.c3equalz.user_service.infrastructure.auth.session.AuthSessionIDGenerator;
import com.c3equalz.user_service.infrastructure.auth.session.UtcAuthSessionTimer;
import com.c3equalz.user_service.infrastructure.auth.session.ports.AuthSessionGateway;
import com.c3equalz.user_service.infrastructure.auth.session.ports.AuthSessionTransport;
import com.c3equalz.user_service.infrastructure.errors.RepoError;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;

import java.time.Duration;

/**
 * Service for managing authentication sessions.
 */
@Slf4j
@RequiredArgsConstructor
public class AuthSessionService {

    private final AuthSessionGateway authSessionGateway;
    private final AuthSessionTransport authSessionTransport;
    private final TransactionManager transactionManager;
    private final AuthSessionIDGenerator authSessionIDGenerator;
    private final UtcAuthSessionTimer authSessionTimer;

    /**
     * Creates a new authentication session for the given user.
     *
     * @param userId the user ID to create session for
     * @return Mono that completes when session is created
     * @throws AuthenticationError if session creation fails
     */
    public Mono<Void> createSession(UserID userId) {
        log.debug("Create auth session: started. User ID: '{}'.", userId);

        String authSessionId = authSessionIDGenerator.generate();
        var expiration = authSessionTimer.authSessionExpiration();
        AuthSession authSession = new AuthSession(
                authSessionId,
                userId,
                expiration
        );

        return authSessionGateway.add(authSession)
                .then(transactionManager.commit())
                .onErrorMap(RepoError.class, error -> {
                    String msg = "Authentication is currently unavailable. Please try again later.";
                    return new AuthenticationError(msg, error);
                })
                .then(authSessionTransport.deliver(authSession))
                .doOnSuccess(v -> log.debug(
                        "Create auth session: done. User ID: '{}', Auth session id: '{}'.",
                        userId,
                        authSession.getId()
                ));
    }

    /**
     * Gets the authenticated user ID from the current session.
     *
     * @return Mono containing the user ID
     * @throws AuthenticationError if session is invalid or expired
     */
    public Mono<UserID> getAuthenticatedUserID() {
        log.debug("Get authenticated user ID: started.");

        return loadCurrentSession()
                .flatMap(this::validateAndExtendSession)
                .doOnSuccess(validSession -> {
                    assert validSession != null;
                    log.debug(
                            "Get authenticated user ID: done. Auth session ID: {}. User ID: {}.",
                            validSession.getId(),
                            validSession.getUserID()
                    );
                })
                .map(AuthSession::getUserID);
    }

    /**
     * Invalidates the current session.
     */
    public Mono<Void> invalidateCurrentSession() {
        log.debug("Invalidate current session: started. Auth session ID: unknown.");

        return authSessionTransport.extractID()
                .flatMap(optionalSessionId -> {
                    if (optionalSessionId.isEmpty()) {
                        log.warn(
                                "Invalidate current session failed: partially failed. " +
                                        "Session ID can't be extracted from transport. " +
                                        "Auth session can't be identified."
                        );
                        return Mono.empty();
                    }

                    String authSessionId = optionalSessionId.get();
                    log.debug(
                            "Invalidate current session: in progress. Auth session id: {}.",
                            authSessionId
                    );

                    return authSessionTransport.removeCurrent()
                            .then(authSessionGateway.readByID(authSessionId))
                            .flatMap(optionalSession -> {
                                if (optionalSession.isEmpty()) {
                                    log.warn(
                                            "Invalidate current session failed: partially failed. " +
                                                    "Session ID was removed from transport, " +
                                                    "but auth session was not found in storage."
                                    );
                                    return Mono.empty();
                                }

                                AuthSession authSession = optionalSession.get();
                                return authSessionGateway.deleteByID(authSession.getId())
                                        .then(transactionManager.commit())
                                        .onErrorResume(RepoError.class, error -> {
                                            log.warn(
                                                    "Invalidate current session failed: partially failed. " +
                                                            "Session ID was removed from transport, " +
                                                            "but auth session was not deleted from storage. " +
                                                            "Auth session ID: '{}'.",
                                                    authSession.getId(),
                                                    error
                                            );
                                            return Mono.empty();
                                        });
                            })
                            .onErrorResume(RepoError.class, error -> {
                                log.error("Auth session extraction failed.", error);
                                return Mono.empty();
                            });
                })
                .then();
    }

    /**
     * Invalidates all sessions for the given user.
     *
     * @param userId the user ID whose sessions should be invalidated
     * @return Mono that completes when all sessions are invalidated
     */
    public Mono<Void> invalidateAllSessionsForUser(UserID userId) {
        log.debug(
                "Invalidate all sessions for user: started. User id: '{}'.",
                userId
        );

        return authSessionGateway.deleteAllForUser(userId)
                .then(transactionManager.commit())
                .doOnSuccess(v -> log.debug(
                        "Invalidate all sessions for user: done. User id: '{}'.",
                        userId
                ));
    }

    /**
     * Loads the current authentication session from transport.
     *
     * @return Mono containing the current session
     * @throws AuthenticationError if session cannot be loaded
     */
    private Mono<AuthSession> loadCurrentSession() {
        log.debug("Load current auth session: started. Auth session id: unknown.");

        return authSessionTransport.extractID()
                .flatMap(optionalSessionId -> {
                    if (optionalSessionId.isEmpty()) {
                        log.debug("Session not found.");
                        return Mono.error(new AuthenticationError("Not authenticated."));
                    }

                    String authSessionId = optionalSessionId.get();
                    log.debug(
                            "Load current auth session: in progress. Auth session id: {}.",
                            authSessionId
                    );

                    return authSessionGateway.readByID(authSessionId)
                            .flatMap(optionalSession -> {
                                if (optionalSession.isEmpty()) {
                                    log.debug("Session not found.");
                                    return Mono.error(new AuthenticationError("Not authenticated."));
                                }

                                AuthSession authSession = optionalSession.get();
                                log.debug(
                                        "Load current auth session: done. Auth session id: {}.",
                                        authSession.getId()
                                );
                                return Mono.just(authSession);
                            })
                            .onErrorMap(RepoError.class, error -> {
                                log.error("Auth session extraction failed.", error);
                                return new AuthenticationError("Not authenticated.", error);
                            });
                });
    }

    /**
     * Validates the session and extends it if necessary.
     *
     * @param authSession the session to validate and extend
     * @return Mono containing the validated (and possibly extended) session
     * @throws AuthenticationError if session is expired
     */
    private Mono<AuthSession> validateAndExtendSession(AuthSession authSession) {
        log.debug(
                "Validate and extend auth session: started. Auth session id: {}.",
                authSession.getId()
        );

        var now = authSessionTimer.currentTime();
        if (authSession.getExpiration().isBefore(now) || authSession.getExpiration().equals(now)) {
            log.debug("Session expired.");
            return Mono.error(new AuthenticationError("Not authenticated."));
        }

        Duration remainingTime = Duration.between(now, authSession.getExpiration());
        Duration refreshTriggerInterval = authSessionTimer.refreshTriggerInterval();

        if (remainingTime.compareTo(refreshTriggerInterval) > 0) {
            log.debug(
                    "Validate and extend auth session: validated without extension. Auth session id: {}.",
                    authSession.getId()
            );
            return Mono.just(authSession);
        }

        // Session needs to be extended
        var originalExpiration = authSession.getExpiration();
        authSession.setExpiration(authSessionTimer.authSessionExpiration());

        return authSessionGateway.update(authSession)
                .then(transactionManager.commit())
                .then(authSessionTransport.deliver(authSession))
                .thenReturn(authSession)
                .onErrorResume(RepoError.class, error -> {
                    log.error("Auth session extension failed.", error);
                    authSession.setExpiration(originalExpiration);
                    return Mono.just(authSession);
                })
                .doOnSuccess(validSession -> {
                    assert validSession != null;
                    log.debug(
                            "Validate and extend auth session: done. Auth session id: {}.",
                            validSession.getId()
                    );
                });
    }
}
