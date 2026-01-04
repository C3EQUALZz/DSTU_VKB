package com.c3equalz.user_service.application.auth.sign_up;

import com.c3equalz.user_service.domain.user.values.UserRole;

/**
 * Data transfer object for user sign up.
 */
public record SignUpData(String email, String name, String password, UserRole role) {
    public SignUpData(String email, String name, String password, UserRole role) {
        this.email = email;
        this.name = name;
        this.password = password;
        this.role = role != null ? role : UserRole.USER;
    }
}
