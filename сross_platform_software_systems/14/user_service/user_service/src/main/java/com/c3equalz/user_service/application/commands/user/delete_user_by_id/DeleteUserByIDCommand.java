package com.c3equalz.user_service.application.commands.user.delete_user_by_id;

import java.util.UUID;

/**
 * Command for deleting a user by ID.
 */
public record DeleteUserByIDCommand(UUID user_id) {
}
