package com.c3equalz.user_service.application.errors;

public class LimitCantBeNegativeError extends ApplicationError {
    public LimitCantBeNegativeError(String message) {
        super(message);
    }

    public LimitCantBeNegativeError(String message, Throwable cause) {
        super(message, cause);
    }
}
