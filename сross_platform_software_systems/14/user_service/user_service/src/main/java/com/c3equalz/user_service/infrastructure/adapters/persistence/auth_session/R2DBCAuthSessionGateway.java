package com.c3equalz.user_service.infrastructure.adapters.persistence.auth_session;

import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.infrastructure.adapters.persistence.constants.DatabaseConstants;
import com.c3equalz.user_service.infrastructure.auth.session.AuthSession;
import com.c3equalz.user_service.infrastructure.auth.session.ports.AuthSessionGateway;
import com.c3equalz.user_service.infrastructure.errors.RepoError;
import io.r2dbc.spi.R2dbcException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.r2dbc.core.DatabaseClient;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

/**
 * R2DBC implementation of AuthSessionGateway.
 * <p>
 * Uses DatabaseClient for reactive database operations.
 * This is a low-level approach similar to SQLAlchemy's AsyncSession.
 */
@Slf4j
@Repository
@RequiredArgsConstructor
public class R2DBCAuthSessionGateway implements AuthSessionGateway {

    private final DatabaseClient databaseClient;

    @Override
    public Mono<Void> add(AuthSession authSession) {
        try {
            String sql = "INSERT INTO auth_sessions (id, user_id, expiration) VALUES (:id, :user_id, :expiration)";
            
            return databaseClient.sql(sql)
                    .bind("id", authSession.getId())
                    .bind("user_id", authSession.getUserID().getValue())
                    .bind("expiration", authSession.getExpiration())
                    .fetch()
                    .rowsUpdated()
                    .flatMap(rowsUpdated -> {
                        if (rowsUpdated == 0) {
                            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED + " No rows inserted."));
                        }
                        return Mono.<Void>empty();
                    })
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to add auth session", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    })
                    .then();
        } catch (Exception e) {
            log.error("Failed to add auth session", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Optional<AuthSession>> readByID(String authSessionID) {
        try {
            String sql = "SELECT id, user_id, expiration FROM auth_sessions WHERE id = :id";
            
            return databaseClient.sql(sql)
                    .bind("id", authSessionID)
                    .map((row, metadata) -> {
                        String id = row.get("id", String.class);
                        UUID userId = row.get("user_id", UUID.class);
                        Instant expiration = row.get("expiration", Instant.class);
                        
                        return new AuthSession(id, new UserID(userId), expiration);
                    })
                    .one()
                    .map(Optional::of)
                    .defaultIfEmpty(Optional.empty())
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to read auth session by ID", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    });
        } catch (Exception e) {
            log.error("Failed to read auth session by ID", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Void> update(AuthSession authSession) {
        try {
            String sql = "UPDATE auth_sessions SET expiration = :expiration WHERE id = :id";
            
            return databaseClient.sql(sql)
                    .bind("expiration", authSession.getExpiration())
                    .bind("id", authSession.getId())
                    .fetch()
                    .rowsUpdated()
                    .flatMap(rowsUpdated -> {
                        if (rowsUpdated == 0) {
                            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED + " No rows updated."));
                        }
                        return Mono.<Void>empty();
                    })
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to update auth session", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    })
                    .then();
        } catch (Exception e) {
            log.error("Failed to update auth session", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Void> deleteByID(String authSessionID) {
        try {
            String sql = "DELETE FROM auth_sessions WHERE id = :id";
            
            return databaseClient.sql(sql)
                    .bind("id", authSessionID)
                    .fetch()
                    .rowsUpdated()
                    .then()
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to delete auth session by ID", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    })
                    .then();
        } catch (Exception e) {
            log.error("Failed to delete auth session by ID", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Void> deleteAllForUser(UserID userID) {
        try {
            String sql = "DELETE FROM auth_sessions WHERE user_id = :user_id";
            
            return databaseClient.sql(sql)
                    .bind("user_id", userID.getValue())
                    .fetch()
                    .rowsUpdated()
                    .then()
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to delete all auth sessions for user", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    })
                    .then();
        } catch (Exception e) {
            log.error("Failed to delete all auth sessions for user", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }
}

