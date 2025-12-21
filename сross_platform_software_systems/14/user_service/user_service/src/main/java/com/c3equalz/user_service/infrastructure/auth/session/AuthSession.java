package com.c3equalz.user_service.infrastructure.auth.session;

import com.c3equalz.user_service.domain.user.values.UserID;
import lombok.Getter;
import lombok.Setter;

import java.time.Instant;

/**
 * This class can become a domain entity in a new bounded context, enabling a monolithic architecture to become modular,
 * while the other classes working with it are likely to become application and infrastructure layer components.
 * For example, `LogInHandler` can become an interactor.
 */
@Getter
@Setter
public class AuthSession {
    private final String id;
    private final UserID userID;
    private Instant expiration;

    public AuthSession(String id, UserID userID, Instant expiration) {
        this.id = id;
        this.userID = userID;
        this.expiration = expiration;
    }
}
