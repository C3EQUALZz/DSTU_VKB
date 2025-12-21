package com.c3equalz.user_service.domain.user.ports;

import com.c3equalz.user_service.domain.user.values.RawPassword;
import com.c3equalz.user_service.domain.user.values.UserPasswordHash;

/**
 * Port for password hashing operations.
 * Provides methods to hash raw passwords and verify them against hashed passwords.
 */
public interface PasswordHasher {

    /**
     * Hashes a raw password.
     *
     * @param rawPassword the raw password to hash
     * @return the hashed password
     */
    UserPasswordHash hash(RawPassword rawPassword);

    /**
     * Verifies a raw password against a hashed password.
     *
     * @param rawPassword the raw password to verify
     * @param hashedPassword the hashed password to verify against
     * @return true if the password matches, false otherwise
     */
    boolean verify(RawPassword rawPassword, UserPasswordHash hashedPassword);
}

