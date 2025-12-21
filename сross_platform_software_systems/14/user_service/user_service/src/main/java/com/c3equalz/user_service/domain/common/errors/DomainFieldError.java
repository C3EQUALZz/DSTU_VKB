package com.c3equalz.user_service.domain.common.errors;

/**
 * Exception raised when domain field validation fails.
 * <p>
 * Indicates that a value assigned to a domain object's field violates
 * business rules or invariants.
 * <p>
 * Note:
 * <ul>
 *     <li>Inherits from DomainError to maintain consistent error handling</li>
 *     <li>Used for validation failures in value objects and entities</li>
 *     <li>Typically caught and converted to appropriate application errors</li>
 *     <li>The default message from DomainError is usually sufficient,
 *         but can be overridden for specific field validation cases</li>
 * </ul>
 */
public class DomainFieldError extends DomainError {

    public DomainFieldError(String message) {
        super(message);
    }

    public DomainFieldError(String message, Throwable cause) {
        super(message, cause);
    }
}

