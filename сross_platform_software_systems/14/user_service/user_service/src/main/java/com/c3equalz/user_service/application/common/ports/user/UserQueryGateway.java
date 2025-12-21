package com.c3equalz.user_service.application.common.ports.user;

/**
 * Gateway for user query operations.
 * <p>
 * This interface is defined to allow easier mocking and swapping of implementations.
 * Currently, query operations may be handled by UserCommandGateway,
 * but a separate interface is provided for future separation of concerns.
 */
public interface UserQueryGateway {
    // Query methods can be added here in the future
    // For now, this interface serves as a placeholder for separation of concerns
}

