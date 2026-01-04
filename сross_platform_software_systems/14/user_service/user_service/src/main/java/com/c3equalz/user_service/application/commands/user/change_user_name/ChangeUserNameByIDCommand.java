package com.c3equalz.user_service.application.commands.user.change_user_name;

import java.util.UUID;

/**
 * Command for changing a user's name by ID.
 */
public record ChangeUserNameByIDCommand(UUID userID, String new_name) {
}

