package com.c3equalz.user_service.setup.config.security;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import org.springframework.validation.annotation.Validated;

/**
 * Password settings loaded from environment variables.
 */
@Getter
@Setter
@Validated
public class PasswordSettings {

    /**
     * Password pepper value for additional security.
     */
    @NotNull(message = "PEPPER must be provided")
    private String pepper;
}

