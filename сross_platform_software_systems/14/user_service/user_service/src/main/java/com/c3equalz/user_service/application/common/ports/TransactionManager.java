package com.c3equalz.user_service.application.common.ports;

import reactor.core.publisher.Mono;

/**
 * Unit of Work-compatible interface for committing a business transaction.
 * The implementation may be an ORM session, such as R2DBC's DatabaseClient
 * or Spring Data R2DBC's ReactiveTransactionManager.
 * <p>
 * For more information, see: https://t.me/advice17/60
 */
public interface TransactionManager {

    /**
     * Save all operations in database.
     * Commits the current transaction.
     *
     * @return Mono that completes when the commit is done
     */
    Mono<Void> commit();

    /**
     * Flush all pending operations to the database without committing.
     * This is useful for getting generated IDs or for validation purposes.
     *
     * @return Mono that completes when the flush is done
     */
    Mono<Void> flush();

    /**
     * Method that rolls back all operations.
     * Reverts all changes made in the current transaction.
     *
     * @return Mono that completes when the rollback is done
     */
    Mono<Void> rollback();
}

