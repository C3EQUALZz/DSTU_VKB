package com.c3equalz.user_service.infrastructure.adapters.persistence.user;

import com.c3equalz.user_service.application.common.ports.user.UserCommandGateway;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.values.UserEmail;
import com.c3equalz.user_service.domain.user.values.UserID;
import com.c3equalz.user_service.infrastructure.adapters.persistence.constants.DatabaseConstants;
import com.c3equalz.user_service.infrastructure.adapters.persistence.user.mapper.UserRowMapper;
import com.c3equalz.user_service.infrastructure.errors.RepoError;
import io.r2dbc.spi.R2dbcException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.r2dbc.core.DatabaseClient;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

import java.util.Optional;

/**
 * R2DBC implementation of UserCommandGateway.
 * <p>
 * Uses DatabaseClient for reactive database operations.
 * This is a low-level approach similar to SQLAlchemy's AsyncSession.
 */
@Slf4j
@Repository
@RequiredArgsConstructor
public class R2DBCUserCommandGateway implements UserCommandGateway {

    private final DatabaseClient databaseClient;
    private final UserRowMapper userRowMapper;

    @Override
    public Mono<Void> add(User user) {
        try {
            String sql = "INSERT INTO users (id, email, name, hashed_password, role, is_active, created_at, updated_at) " +
                    "VALUES (:id, :email, :name, :hashed_password, :role, :is_active, :created_at, :updated_at)";

            return databaseClient.sql(sql)
                    .bind("id", user.getId().getValue())
                    .bind("email", user.getEmail().getValue())
                    .bind("name", user.getName().getValue())
                    .bind("hashed_password", user.getHashedPassword().getValue())
                    .bind("role", user.getRole().toString())
                    .bind("is_active", user.isActive())
                    .bind("created_at", user.getCreatedAt())
                    .bind("updated_at", user.getUpdatedAt())
                    .fetch()
                    .rowsUpdated()
                    .flatMap(rowsUpdated -> {
                        if (rowsUpdated == 0) {
                            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED + " No rows inserted."));
                        }
                        return Mono.<Void>empty();
                    })
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to add user", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    })
                    .then();
        } catch (Exception e) {
            log.error("Failed to add user", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Optional<User>> readById(UserID userId) {
        try {
            String sql = "SELECT id, email, name, hashed_password, role, is_active, created_at, updated_at " +
                    "FROM users WHERE id = :id";

            return databaseClient.sql(sql)
                    .bind("id", userId.getValue())
                    .map((row, _) -> userRowMapper.rowToEntity(row))
                    .one()
                    .map(Optional::of)
                    .defaultIfEmpty(Optional.empty())
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to read user by ID", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    });
        } catch (Exception e) {
            log.error("Failed to read user by ID", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Optional<User>> readByEmail(UserEmail userEmail) {
        try {
            String sql = "SELECT id, email, name, hashed_password, role, is_active, created_at, updated_at " +
                    "FROM users WHERE email = :email";

            return databaseClient.sql(sql)
                    .bind("email", userEmail.getValue())
                    .map((row, _) -> userRowMapper.rowToEntity(row))
                    .one()
                    .map(Optional::of)
                    .defaultIfEmpty(Optional.empty())
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to read user by email", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    });
        } catch (Exception e) {
            log.error("Failed to read user by email", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Void> deleteByID(UserID userID) {
        try {
            String sql = "DELETE FROM users WHERE id = :id";

            return databaseClient.sql(sql)
                    .bind("id", userID.getValue())
                    .fetch()
                    .rowsUpdated()
                    .then()
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to delete user by ID", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    })
                    .then();
        } catch (Exception e) {
            log.error("Failed to delete user by ID", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }

    @Override
    public Mono<Void> update(User user) {
        try {
            String sql = "UPDATE users SET " +
                    "email = :email, " +
                    "name = :name, " +
                    "hashed_password = :hashed_password, " +
                    "role = :role, " +
                    "is_active = :is_active, " +
                    "updated_at = :updated_at " +
                    "WHERE id = :id";

            return databaseClient.sql(sql)
                    .bind("email", user.getEmail().getValue())
                    .bind("name", user.getName().getValue())
                    .bind("hashed_password", user.getHashedPassword().getValue())
                    .bind("role", user.getRole().toString())
                    .bind("is_active", user.isActive())
                    .bind("updated_at", user.getUpdatedAt())
                    .bind("id", user.getId().getValue())
                    .fetch()
                    .rowsUpdated()
                    .flatMap(rowsUpdated -> {
                        if (rowsUpdated == 0) {
                            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED + " No rows updated."));
                        }
                        return Mono.<Void>empty();
                    })
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to update user", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    })
                    .then();
        } catch (Exception e) {
            log.error("Failed to update user", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }
}
