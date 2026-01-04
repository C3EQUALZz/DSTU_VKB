package com.c3equalz.user_service.application.errors.user;

import com.c3equalz.user_service.application.errors.ApplicationError;

/**
 * Exception thrown when a user is not found by ID.
 */
public class UserNotFoundByIDError extends ApplicationError {

    public UserNotFoundByIDError(String message) {
        super(message);
    }

    public UserNotFoundByIDError(String message, Throwable cause) {
        super(message, cause);
    }
}

