package com.c3equalz.user_service.domain.common.errors;

/**
 * Base exception class for domain layer errors.
 * <p>
 * Provides a consistent interface for error messages across all
 * domain-specific exceptions. All domain-level errors should inherit from this class.
 * <p>
 * Note:
 * <ul>
 *     <li>Serves as the root of the domain error hierarchy</li>
 *     <li>Provides consistent error message interface</li>
 *     <li>Follows the convention of rich exceptions with additional attributes</li>
 * </ul>
 */
public class DomainError extends AppError {

    public DomainError(String message) {
        super(message);
    }

    public DomainError(String message, Throwable cause) {
        super(message, cause);
    }
}

