package com.c3equalz.user_service.application.common.views.user;

import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.UUID;

/**
 * View representation of a user for reading by ID.
 */
@Getter
@AllArgsConstructor
public class ReadUserByIDView {
    private final UUID id;
    private final String email;
    private final String name;
    private final UserRole role;
}

