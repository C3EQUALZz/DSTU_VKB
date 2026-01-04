package com.c3equalz.user_service.infrastructure.adapters.persistence.user.mapper;

import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.values.*;
import io.r2dbc.spi.Row;
import org.mapstruct.Mapper;
import org.mapstruct.Named;

import java.util.UUID;

/**
 * MapStruct mapper for converting database Row data to User entity.
 * <p>
 * This mapper encapsulates the logic of mapping database rows to domain entities,
 * eliminating code duplication across repositories.
 * <p>
 * Uses Spring component model for dependency injection.
 */
@Mapper(componentModel = "spring")
public interface UserRowMapper {

    /**
     * Maps a database Row to UserRowDTO.
     *
     * @param row the database row
     * @return UserRowDTO containing extracted data
     */
    default UserRowDTO rowToDTO(Row row) {
        return new UserRowDTO(
                row.get("id", java.util.UUID.class),
                row.get("email", String.class),
                row.get("name", String.class),
                row.get("hashed_password", byte[].class),
                row.get("role", String.class),
                row.get("is_active", Boolean.class),
                row.get("created_at", java.time.Instant.class),
                row.get("updated_at", java.time.Instant.class)
        );
    }

    /**
     * Maps UserRowDTO to User entity.
     * Note: This method uses manual mapping due to complex value object creation.
     *
     * @param dto the data transfer object
     * @return User domain entity
     */
    default User dtoToEntity(UserRowDTO dto) {
        User user = new User(
                uuidToUserID(dto.id()),
                stringToUserEmail(dto.email()),
                stringToUsername(dto.name()),
                bytesToUserPasswordHash(dto.hashedPassword()),
                stringToUserRole(dto.role())
        );
        user.setActive(Boolean.TRUE.equals(dto.isActive()));
        user.setCreatedAt(dto.createdAt());
        user.setUpdatedAt(dto.updatedAt());
        return user;
    }

    /**
     * Maps a database Row directly to User entity.
     * This is the main method to use in repositories.
     *
     * @param row the database row
     * @return User domain entity
     */
    default User rowToEntity(Row row) {
        UserRowDTO dto = rowToDTO(row);
        return dtoToEntity(dto);
    }

    @Named("uuidToUserID")
    default UserID uuidToUserID(UUID id) {
        return new UserID(id);
    }

    @Named("stringToUserEmail")
    default UserEmail stringToUserEmail(String email) {
        return new UserEmail(email);
    }

    @Named("stringToUsername")
    default Username stringToUsername(String name) {
        return new Username(name);
    }

    @Named("bytesToUserPasswordHash")
    default UserPasswordHash bytesToUserPasswordHash(byte[] hashedPassword) {
        return new UserPasswordHash(hashedPassword);
    }

    @Named("stringToUserRole")
    default UserRole stringToUserRole(String roleStr) {
        // Convert "super_admin" -> "SUPER_ADMIN" for enum
        String enumName = roleStr.toUpperCase().replace("-", "_");
        return UserRole.valueOf(enumName);
    }

}

