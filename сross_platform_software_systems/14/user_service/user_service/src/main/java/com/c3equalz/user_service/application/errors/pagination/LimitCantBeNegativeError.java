package com.c3equalz.user_service.application.errors.pagination;

import com.c3equalz.user_service.application.errors.ApplicationError;

public class LimitCantBeNegativeError extends ApplicationError {
    public LimitCantBeNegativeError(String message) {
        super(message);
    }

    public LimitCantBeNegativeError(String message, Throwable cause) {
        super(message, cause);
    }
}
