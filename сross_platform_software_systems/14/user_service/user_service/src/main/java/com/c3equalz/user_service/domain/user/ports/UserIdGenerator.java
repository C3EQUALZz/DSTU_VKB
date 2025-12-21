package com.c3equalz.user_service.domain.user.ports;

import com.c3equalz.user_service.domain.user.values.UserID;

/**
 * Port for generating user IDs.
 * Provides a method to generate unique user identifiers.
 */
@FunctionalInterface
public interface UserIdGenerator {

    /**
     * Generates a new unique user ID.
     *
     * @return a new UserID instance
     */
    UserID generate();
}

