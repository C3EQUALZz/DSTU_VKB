package com.c3equalz.user_service.application.common.ports.user;

import com.c3equalz.user_service.application.common.query_params.user.UserListParams;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.values.UserID;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Optional;

/**
 * Gateway for user query operations.
 * <p>
 * This interface is defined to allow easier mocking and swapping of implementations.
 * Separates query operations from command operations following CQRS pattern.
 */
public interface UserQueryGateway {

    /**
     * Reads a user by ID.
     *
     * @param user_id the user ID to read
     * @return Mono containing the user, or empty Mono if not found
     */
    Mono<Optional<User>> readUserById(UserID user_id);

    /**
     * Reads all users with pagination and sorting.
     *
     * @param userListParams parameters for filtering, pagination and sorting
     * @return Mono containing list of users, or empty list if none found
     */
    Mono<List<User>> readAllUsers(UserListParams userListParams);
}



