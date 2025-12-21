package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

/**
 * Exception thrown when a weak password is provided.
 * This includes passwords that are too short, too long, or contain only digits.
 */
public class WeakPasswordWasProvidedError extends DomainFieldError {

    public WeakPasswordWasProvidedError(String message) {
        super(message);
    }

    public WeakPasswordWasProvidedError(String message, Throwable cause) {
        super(message, cause);
    }
}

