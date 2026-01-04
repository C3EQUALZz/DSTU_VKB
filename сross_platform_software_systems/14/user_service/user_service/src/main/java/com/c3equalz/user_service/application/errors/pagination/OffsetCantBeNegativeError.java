package com.c3equalz.user_service.application.errors.pagination;

import com.c3equalz.user_service.application.errors.ApplicationError;

public class OffsetCantBeNegativeError extends ApplicationError {
    public OffsetCantBeNegativeError(String message) {
        super(message);
    }

    public OffsetCantBeNegativeError(String message, Throwable cause) {
        super(message, cause);
    }
}
