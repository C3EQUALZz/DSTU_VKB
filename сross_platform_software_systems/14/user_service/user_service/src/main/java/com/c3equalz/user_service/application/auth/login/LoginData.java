package com.c3equalz.user_service.application.auth.login;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Getter
public class LoginData {
    private final String password;
    private final String email;
}
