package com.c3equalz.user_service.application.errors;

import com.c3equalz.user_service.domain.common.errors.AppError;

public class ApplicationError extends AppError {
    public ApplicationError(String message) {
        super(message);
    }

    public ApplicationError(String message, Throwable cause) {
        super(message, cause);
    }
}
