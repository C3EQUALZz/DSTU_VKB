package com.c3equalz.user_service.application.commands.user.create_user;

import com.c3equalz.user_service.domain.user.values.UserRole;

/**
 * Command for creating a new user.
 */
public record CreateUserCommand(
        String email,
        String name,
        String password,
        UserRole role
) {
    /**
     * Constructor with default role USER if role is null.
     */
    public CreateUserCommand {
        if (role == null) {
            role = UserRole.USER;
        }
    }

    /**
     * Constructor without role parameter (defaults to USER).
     */
    public CreateUserCommand(String email, String name, String password) {
        this(email, name, password, UserRole.USER);
    }
}
