package com.c3equalz.user_service.domain.common.errors;

/**
 * Base error class for application errors.
 * All application-specific exceptions should inherit from this class.
 */
public class AppError extends RuntimeException {

    public AppError(String message) {
        super(message);
    }

    public AppError(String message, Throwable cause) {
        super(message, cause);
    }
}

