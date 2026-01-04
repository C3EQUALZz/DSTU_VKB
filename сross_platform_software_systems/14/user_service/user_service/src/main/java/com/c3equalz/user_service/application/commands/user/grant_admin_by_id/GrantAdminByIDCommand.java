package com.c3equalz.user_service.application.commands.user.grant_admin_by_id;

import java.util.UUID;

/**
 * Command for granting admin rights to a user by ID.
 */
public record GrantAdminByIDCommand(UUID user_id) {
}
