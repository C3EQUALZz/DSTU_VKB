package com.c3equalz.user_service.setup.config.security;

import lombok.Getter;
import lombok.Setter;
import org.springframework.validation.annotation.Validated;

/**
 * Cookies settings loaded from environment variables.
 */
@Getter
@Setter
@Validated
public class CookiesSettings {

    /**
     * Whether cookies should be sent only over secure connections (HTTPS).
     */
    private boolean secure = false;
}

