package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

/**
 * Exception thrown when an empty password is provided.
 */
public class EmptyPasswordWasProvidedError extends DomainFieldError {

    public EmptyPasswordWasProvidedError(String message) {
        super(message);
    }

    public EmptyPasswordWasProvidedError(String message, Throwable cause) {
        super(message, cause);
    }
}

