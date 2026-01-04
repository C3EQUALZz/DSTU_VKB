package com.c3equalz.user_service.application.common.views.auth;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.UUID;

/**
 * View representation of a sign up result.
 */
@Getter
@AllArgsConstructor
public class SignUpView {
    private final UUID user_id;
}



