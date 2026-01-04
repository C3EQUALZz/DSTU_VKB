package com.c3equalz.user_service.application.commands.user.acitvate_user;

import java.util.UUID;

/**
 * Command for activating a user.
 */
public record ActivateUserCommand(UUID userID) { }
