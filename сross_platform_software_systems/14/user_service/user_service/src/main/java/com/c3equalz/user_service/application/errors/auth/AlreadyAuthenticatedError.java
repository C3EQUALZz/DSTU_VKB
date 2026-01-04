package com.c3equalz.user_service.application.errors.auth;

import com.c3equalz.user_service.application.errors.ApplicationError;

/**
 * Exception thrown when a user tries to authenticate while already authenticated.
 */
public class AlreadyAuthenticatedError extends ApplicationError {

    public AlreadyAuthenticatedError(String message) {
        super(message);
    }

    public AlreadyAuthenticatedError(String message, Throwable cause) {
        super(message, cause);
    }
}

