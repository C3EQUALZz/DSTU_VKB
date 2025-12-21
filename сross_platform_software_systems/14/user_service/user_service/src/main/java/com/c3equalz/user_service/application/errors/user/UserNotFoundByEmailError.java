package com.c3equalz.user_service.application.errors.user;

import com.c3equalz.user_service.application.errors.ApplicationError;

/**
 * Exception thrown when a user is not found by email.
 */
public class UserNotFoundByEmailError extends ApplicationError {

    public UserNotFoundByEmailError(String message) {
        super(message);
    }

    public UserNotFoundByEmailError(String message, Throwable cause) {
        super(message, cause);
    }
}

