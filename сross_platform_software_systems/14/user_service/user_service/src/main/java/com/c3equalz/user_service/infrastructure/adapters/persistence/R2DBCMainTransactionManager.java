package com.c3equalz.user_service.infrastructure.adapters.persistence;

import com.c3equalz.user_service.application.common.ports.TransactionManager;
import com.c3equalz.user_service.infrastructure.adapters.persistence.constants.DatabaseConstants;
import com.c3equalz.user_service.infrastructure.errors.EntityAddError;
import com.c3equalz.user_service.infrastructure.errors.RepoError;
import com.c3equalz.user_service.infrastructure.errors.RollbackError;
import io.r2dbc.spi.R2dbcException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Component;
import org.springframework.transaction.reactive.TransactionalOperator;
import reactor.core.publisher.Mono;

/**
 * R2DBC implementation of TransactionManager using TransactionOperator.
 * <p>
 * This implementation uses Spring's TransactionOperator for managing transactions
 * programmatically without requiring @Transactional annotations in application layer.
 * The TransactionOperator must be used to wrap handler calls at the infrastructure/presentation
 * layer (e.g., in controllers or adapters), while handlers remain framework-agnostic.
 * <p>
 * Note: In R2DBC with TransactionOperator, transactions commit automatically when the reactive
 * chain completes successfully, and roll back automatically when an error occurs. The commit()
 * and rollback() methods in this class are provided for API compatibility with the Unit of Work
 * pattern, but the actual transaction management is handled by TransactionOperator.
 * <p>
 * Error handling: Errors that occur in the reactive chain (such as constraint violations) are
 * automatically handled by TransactionOperator (rollback). The error conversion to domain exceptions
 * (EntityAddError, RepoError) should be done in Gateway implementations using onErrorMap.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class R2DBCMainTransactionManager implements TransactionManager {

    private final TransactionalOperator transactionalOperator;

    /**
     * Commits the current transaction.
     * <p>
     * In R2DBC with TransactionOperator, transactions commit automatically when the reactive
     * chain completes successfully. This method logs the commit operation for API compatibility
     * with the Unit of Work pattern. The actual commit is handled by TransactionOperator when
     * the reactive chain completes successfully.
     *
     * @return Mono that completes immediately
     */
    @Override
    public Mono<Void> commit() {
        log.debug("{} Main session.", DatabaseConstants.DB_COMMIT_DONE);
        // TransactionOperator commits automatically when reactive chain completes successfully
        return Mono.empty();
    }

    /**
     * Flushes pending operations to the database without committing.
     * <p>
     * In R2DBC, all SQL operations are executed immediately, so there is no
     * concept of "pending operations" to flush. This method is implemented
     * as a no-op for API compatibility with the Unit of Work pattern.
     *
     * @return Mono that completes immediately
     */
    @Override
    public Mono<Void> flush() {
        log.debug("{} Main session.", DatabaseConstants.DB_FLUSH_DONE);
        // In R2DBC, there's no flush concept - all operations execute immediately
        return Mono.empty();
    }

    /**
     * Rolls back the current transaction.
     * <p>
     * In R2DBC with TransactionOperator, transactions roll back automatically when an error
     * occurs in the reactive chain. To trigger a rollback, throw an exception in the reactive chain.
     * This method logs the rollback operation for API compatibility.
     *
     * @return Mono that completes immediately
     */
    @Override
    public Mono<Void> rollback() {
        log.debug(DatabaseConstants.DB_ROLLBACK_DONE);
        // TransactionOperator rolls back automatically when an error occurs in reactive chain
        return Mono.empty();
    }

    /**
     * Checks if an R2dbcException represents a constraint violation.
     * <p>
     * PostgreSQL error codes for constraint violations:
     * - 23503: foreign_key_violation
     * - 23505: unique_violation
     * - 23514: check_violation
     * - 23502: not_null_violation
     *
     * @param exception the R2dbcException to check
     * @return true if the exception represents a constraint violation
     */
    static boolean isConstraintViolation(R2dbcException exception) {
        int errorCode = exception.getErrorCode();
        return errorCode == 23503  // foreign_key_violation
                || errorCode == 23505  // unique_violation
                || errorCode == 23514  // check_violation
                || errorCode == 23502; // not_null_violation
    }

    /**
     * Converts a database exception to an appropriate domain exception.
     * <p>
     * This helper method can be used in Gateway implementations to convert R2dbcException
     * to domain exceptions (EntityAddError for constraint violations, RepoError for other errors).
     *
     * @param exception the R2dbcException to convert
     * @return the appropriate domain exception
     */
    static RuntimeException convertToDomainException(R2dbcException exception) {
        if (isConstraintViolation(exception)) {
            log.error(DatabaseConstants.DB_CONSTRAINT_VIOLATION, exception);
            return new EntityAddError(DatabaseConstants.DB_CONSTRAINT_VIOLATION, exception);
        }
        log.error(DatabaseConstants.DB_CONFLICT, exception);
        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, exception);
    }
}
