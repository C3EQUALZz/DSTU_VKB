package com.c3equalz.user_service.setup.config.security;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

/**
 * Security configuration containing all security-related settings.
 */
@Getter
@Setter
@Validated
@ConfigurationProperties(prefix = "security")
public class SecurityConfig {

    /**
     * Authentication settings.
     */
    @NotNull(message = "Auth settings must be provided")
    @Valid
    private AuthSettings auth;

    /**
     * Cookies settings.
     */
    @NotNull(message = "Cookies settings must be provided")
    @Valid
    private CookiesSettings cookies;

    /**
     * Password settings.
     */
    @NotNull(message = "Password settings must be provided")
    @Valid
    private PasswordSettings password;
}

