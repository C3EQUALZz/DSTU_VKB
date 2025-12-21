package com.c3equalz.user_service.application.errors;

/**
 * Exception thrown when authentication fails.
 */
public class AuthenticationError extends ApplicationError {

    public AuthenticationError(String message) {
        super(message);
    }

    public AuthenticationError(String message, Throwable cause) {
        super(message, cause);
    }
}

