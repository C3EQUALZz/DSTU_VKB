package com.c3equalz.user_service.application.common.views.user;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.UUID;

/**
 * View representation of a created user result.
 */
@Getter
@AllArgsConstructor
public class CreateUserView {
    private final UUID user_id;
}

