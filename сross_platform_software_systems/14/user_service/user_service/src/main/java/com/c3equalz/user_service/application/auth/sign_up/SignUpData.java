package com.c3equalz.user_service.application.auth.sign_up;

import com.c3equalz.user_service.domain.user.values.UserRole;
import lombok.Getter;

/**
 * Data transfer object for user sign up.
 */
@Getter
public class SignUpData {
    private final String email;
    private final String name;
    private final String password;
    private final UserRole role;

    public SignUpData(String email, String name, String password, UserRole role) {
        this.email = email;
        this.name = name;
        this.password = password;
        this.role = role != null ? role : UserRole.USER;
    }

    public SignUpData(String email, String name, String password) {
        this(email, name, password, UserRole.USER);
    }
}
