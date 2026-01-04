package com.c3equalz.user_service.application.errors.user;

import com.c3equalz.user_service.application.errors.ApplicationError;

/**
 * Exception thrown when a user already exists (e.g., by email).
 */
public class UserAlreadyExistsError extends ApplicationError {

    public UserAlreadyExistsError(String message) {
        super(message);
    }

    public UserAlreadyExistsError(String message, Throwable cause) {
        super(message, cause);
    }
}



