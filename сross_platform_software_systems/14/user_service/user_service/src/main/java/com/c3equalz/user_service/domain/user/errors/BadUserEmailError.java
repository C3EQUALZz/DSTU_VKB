package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

public class BadUserEmailError extends DomainFieldError {
    public BadUserEmailError(String message) {
        super(message);
    }

    public BadUserEmailError(String message, Throwable cause) {
        super(message, cause);
    }
}
