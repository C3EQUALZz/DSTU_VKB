package com.c3equalz.user_service.infrastructure.auth.session;

public interface AuthSessionIDGenerator {
    /**
     * Generates unique ID for auth session
     *
     * @return String ID
     */
    String generate();
}
