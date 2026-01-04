package com.c3equalz.user_service.application.commands.user.revoke_admin_by_id;

import java.util.UUID;

/**
 * Command for revoking admin rights from a user by ID.
 */
public record RevokeAdminByIDCommand(UUID user_id) {
}
