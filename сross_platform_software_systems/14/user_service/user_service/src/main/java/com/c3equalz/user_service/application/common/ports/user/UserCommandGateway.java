package com.c3equalz.user_service.application.common.ports.user;

import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.values.UserEmail;
import com.c3equalz.user_service.domain.user.values.UserID;
import reactor.core.publisher.Mono;

import java.util.Optional;

/**
 * Gateway for user command operations.
 */
public interface UserCommandGateway {

    /**
     * Reads a user by ID.
     *
     * @param userId the user ID to read
     * @return Mono containing the user, or Mono.empty() if not found
     */
    Mono<Optional<User>> readById(UserID userId);

    /**
     * Reads a user by email.
     *
     * @param userEmail the user email to read
     * @return Mono containing the user, or Mono.empty() if not found
     */
    Mono<Optional<User>> readByEmail(UserEmail userEmail);

    /**
     * Delete user by ID.
     * @param userID the user ID to delete
     * @return Mono containing Void
     */
    Mono<Void> deleteByID(UserID userID);

    /**
     * Update user in storage
     * @param user Entity to update in storage
     * @return Mono containing Void
     */
    Mono<Void> update(User user);

    /**
     * Add user in storage
     * @param user Entity to add in storage
     * @return Mono containing Void
     */
    Mono<Void> add(User user);
}
