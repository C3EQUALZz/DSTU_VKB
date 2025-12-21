package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

/**
 * Exception thrown when changing user role is not permitted.
 */
public class RoleChangeNotPermittedError extends DomainFieldError {

    public RoleChangeNotPermittedError(String message) {
        super(message);
    }

    public RoleChangeNotPermittedError(String message, Throwable cause) {
        super(message, cause);
    }
}

