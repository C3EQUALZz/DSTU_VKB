package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

/**
 * Exception thrown when a username does not pass domain validation
 */
public class BadUsernameError extends DomainFieldError {
    public BadUsernameError(String message) {
        super(message);
    }

    public BadUsernameError(String message, Throwable cause) {
        super(message, cause);
    }
}
