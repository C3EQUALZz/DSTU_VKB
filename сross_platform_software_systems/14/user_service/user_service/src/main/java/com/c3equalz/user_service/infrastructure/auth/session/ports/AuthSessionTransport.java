package com.c3equalz.user_service.infrastructure.auth.session.ports;

import com.c3equalz.user_service.infrastructure.auth.session.AuthSession;
import reactor.core.publisher.Mono;

import java.util.Optional;

public interface AuthSessionTransport {
    Mono<Void> deliver(AuthSession authSession);

    Mono<Optional<String>> extractID();

    Mono<Void> removeCurrent();
}
