package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainError;

/**
 * Exception thrown when authorization fails.
 */
public class AuthorizationError extends DomainError {

    public AuthorizationError(String message) {
        super(message);
    }

    public AuthorizationError(String message, Throwable cause) {
        super(message, cause);
    }
}

