package com.c3equalz.user_service.infrastructure.adapters.persistence.user.mapper;

import java.time.Instant;
import java.util.UUID;

/**
 * Data Transfer Object for user row data from database.
 * Used as intermediate representation between Row and User entity.
 */
public record UserRowDTO(
        UUID id,
        String email,
        String name,
        byte[] hashedPassword,
        String role,
        Boolean isActive,
        Instant createdAt,
        Instant updatedAt
) {
}

