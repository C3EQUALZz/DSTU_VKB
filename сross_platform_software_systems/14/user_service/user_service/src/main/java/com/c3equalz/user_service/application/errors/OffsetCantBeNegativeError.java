package com.c3equalz.user_service.application.errors;

public class OffsetCantBeNegativeError extends ApplicationError {
    public OffsetCantBeNegativeError(String message) {
        super(message);
    }

    public OffsetCantBeNegativeError(String message, Throwable cause) {
        super(message, cause);
    }
}
