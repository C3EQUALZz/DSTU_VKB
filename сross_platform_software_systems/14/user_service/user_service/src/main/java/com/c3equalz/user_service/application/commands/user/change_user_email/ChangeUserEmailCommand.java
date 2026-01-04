package com.c3equalz.user_service.application.commands.user.change_user_email;

import java.util.UUID;

/**
 * Command for changing a user's email by ID.
 */
public record ChangeUserEmailCommand(UUID user_id, String new_email) {
}
