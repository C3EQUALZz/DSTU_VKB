package com.c3equalz.user_service.infrastructure.adapters.persistence.user;

import com.c3equalz.user_service.application.common.ports.user.UserQueryGateway;
import com.c3equalz.user_service.application.common.query_params.SortingOrder;
import com.c3equalz.user_service.application.common.query_params.user.UserListParams;
import com.c3equalz.user_service.application.common.query_params.user.UserSortingField;
import com.c3equalz.user_service.domain.user.entities.User;
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

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * R2DBC implementation of UserQueryGateway.
 * <p>
 * Uses DatabaseClient for reactive database query operations.
 */
@Slf4j
@Repository
@RequiredArgsConstructor
public class R2DBCUserQueryGateway implements UserQueryGateway {

    private final DatabaseClient databaseClient;
    private final UserRowMapper userRowMapper;

    @Override
    public Mono<Optional<User>> readUserById(UserID user_id) {
        try {
            String sql = "SELECT id, email, name, hashed_password, role, is_active, created_at, updated_at " +
                    "FROM users WHERE id = :id";

            return databaseClient.sql(sql)
                    .bind("id", user_id.getValue())
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
    public Mono<List<User>> readAllUsers(UserListParams userListParams) {
        try {
            UserSortingField sortingField = userListParams.getUserListSorting().getSortingField();
            SortingOrder sortingOrder = userListParams.getUserListSorting().getSortingOrder();
            int offset = userListParams.getPagination().getOffset();
            int limit = userListParams.getPagination().getLimit();

            String sortColumn = sortingField.getValue();
            String sortDirection = sortingOrder == SortingOrder.ASC ? "ASC" : "DESC";

            String sql = String.format(
                    "SELECT id, email, name, hashed_password, role, is_active, created_at, updated_at " +
                            "FROM users " +
                            "ORDER BY %s %s " +
                            "LIMIT :limit OFFSET :offset",
                    sortColumn, sortDirection
            );

            return databaseClient.sql(sql)
                    .bind("limit", limit)
                    .bind("offset", offset)
                    .map((row, _) -> userRowMapper.rowToEntity(row))
                    .all()
                    .collectList()
                    .defaultIfEmpty(new ArrayList<>())
                    .onErrorMap(R2dbcException.class, error -> {
                        log.error("Failed to read all users", error);
                        return new RepoError(DatabaseConstants.DB_QUERY_FAILED, error);
                    });
        } catch (Exception e) {
            log.error("Failed to read all users", e);
            return Mono.error(new RepoError(DatabaseConstants.DB_QUERY_FAILED, e));
        }
    }
}
