package com.c3equalz.user_service.infrastructure.auth.session.ports;

import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.infrastructure.auth.session.AuthSession;
import reactor.core.publisher.Mono;

import java.util.Optional;

/**
 * Defined to allow easier mocking and swapping of implementations in the same layer.
 */
public interface AuthSessionGateway {
    Mono<Void> add(AuthSession authSession);

    Mono<Optional<AuthSession>> readByID(String authSessionID);

    Mono<Void> update(AuthSession authSession);

    Mono<Void> deleteByID(String authSessionID);

    Mono<Void> deleteAllForUser(UserID userID);
}
