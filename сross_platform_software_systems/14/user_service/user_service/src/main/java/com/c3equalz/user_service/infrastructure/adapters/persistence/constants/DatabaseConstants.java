package com.c3equalz.user_service.infrastructure.adapters.persistence.constants;

/**
 * Constants for database operations.
 */
public final class DatabaseConstants {
    /**
     * Error message when a database query fails.
     */
    public static final String DB_QUERY_FAILED = "Database query failed.";

    /**
     * Message when commit is done.
     */
    public static final String DB_COMMIT_DONE = "Commit done.";

    /**
     * Message when flush is done.
     */
    public static final String DB_FLUSH_DONE = "Flush done.";

    /**
     * Message when flush failed.
     */
    public static final String DB_FLUSH_FAILED = "Flush failed.";

    /**
     * Message when rollback is done.
     */
    public static final String DB_ROLLBACK_DONE = "Rollback done.";

    /**
     * Message when rollback failed.
     */
    public static final String DB_ROLLBACK_FAILED = "Rollback failed.";

    /**
     * Message when there is a constraint violation.
     */
    public static final String DB_CONSTRAINT_VIOLATION = "Constraint violation.";

    /**
     * Message when there is a conflict.
     */
    public static final String DB_CONFLICT = "Conflict.";

    private DatabaseConstants() {
        // Utility class - prevent instantiation
    }
}

