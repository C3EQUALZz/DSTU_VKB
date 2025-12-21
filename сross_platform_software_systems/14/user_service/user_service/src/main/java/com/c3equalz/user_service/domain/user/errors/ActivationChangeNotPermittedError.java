package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

/**
 * Exception thrown when changing user activation is not permitted.
 */
public class ActivationChangeNotPermittedError extends DomainFieldError {

    public ActivationChangeNotPermittedError(String message) {
        super(message);
    }

    public ActivationChangeNotPermittedError(String message, Throwable cause) {
        super(message, cause);
    }
}

