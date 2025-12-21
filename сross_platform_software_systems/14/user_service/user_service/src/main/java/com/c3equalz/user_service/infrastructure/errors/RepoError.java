package com.c3equalz.user_service.infrastructure.errors;

import com.c3equalz.user_service.domain.common.errors.AppError;

/**
 * Exception thrown when repository operations fail.
 */
public class RepoError extends AppError {

    public RepoError(String message) {
        super(message);
    }

    public RepoError(String message, Throwable cause) {
        super(message, cause);
    }
}

