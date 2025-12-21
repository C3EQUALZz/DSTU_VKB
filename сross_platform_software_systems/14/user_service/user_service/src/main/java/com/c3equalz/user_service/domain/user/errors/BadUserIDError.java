package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

public class BadUserIDError extends DomainFieldError  {
    public BadUserIDError(String message) {
        super(message);
    }

    public BadUserIDError(String message, Throwable cause) {
        super(message, cause);
    }
}
