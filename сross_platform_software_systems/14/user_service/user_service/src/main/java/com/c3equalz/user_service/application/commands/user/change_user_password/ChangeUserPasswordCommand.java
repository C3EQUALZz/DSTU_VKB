package com.c3equalz.user_service.application.commands.user.change_user_password;

import java.util.UUID;

/**
 * Command for changing a user's password by ID.
 */
public record ChangeUserPasswordCommand(UUID user_id, String password) {
}
