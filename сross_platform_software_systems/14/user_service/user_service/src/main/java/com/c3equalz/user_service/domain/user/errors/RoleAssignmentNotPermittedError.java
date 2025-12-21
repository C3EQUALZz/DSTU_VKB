package com.c3equalz.user_service.domain.user.errors;

import com.c3equalz.user_service.domain.common.errors.DomainFieldError;

/**
 * Exception thrown when assignment of a role is not permitted.
 */
public class RoleAssignmentNotPermittedError extends DomainFieldError {

    public RoleAssignmentNotPermittedError(String message) {
        super(message);
    }

    public RoleAssignmentNotPermittedError(String message, Throwable cause) {
        super(message, cause);
    }
}

