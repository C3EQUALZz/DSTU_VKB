package com.c3equalz.user_service.application.constants;

/**
 * Constants for authentication-related error messages.
 */
public final class AuthConstants {

    public static final String AUTH_ACCOUNT_INACTIVE = "Account is inactive.";
    public static final String AUTH_ALREADY_AUTHENTICATED = "Already authenticated.";
    public static final String AUTH_INVALID_PASSWORD = "Invalid password.";
    public static final String USER_NOT_FOUND = "User not found";

    private AuthConstants() {
        // Prevent instantiation
    }
}

