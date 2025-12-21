package com.c3equalz.user_service.setup.config.security;

import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.convert.DurationUnit;
import org.springframework.validation.annotation.Validated;

import java.time.Duration;
import java.time.temporal.ChronoUnit;

/**
 * Authentication settings loaded from environment variables.
 */
@Getter
@Setter
@Validated
public class AuthSettings {

    /**
     * JWT secret key for signing tokens.
     */
    @NotNull(message = "JWT_SECRET must be provided")
    private String jwtSecret;

    /**
     * JWT algorithm for signing tokens.
     */
    @NotNull(message = "JWT_ALGORITHM must be provided")
    private JwtAlgorithm jwtAlgorithm;

    /**
     * Session time-to-live in minutes.
     * Must be at least 1 minute.
     */
    @NotNull(message = "SESSION_TTL_MIN must be provided")
    @DurationUnit(ChronoUnit.MINUTES)
    private Duration sessionTtlMin;

    /**
     * Validates that sessionTtlMin is at least 1 minute.
     */
    @AssertTrue(message = "SESSION_TTL_MIN must be at least 1 minute")
    public boolean isSessionTtlMinValid() {
        return sessionTtlMin == null || sessionTtlMin.toMinutes() >= 1;
    }

    /**
     * Session refresh threshold (0 < threshold < 1).
     * Determines when to refresh the session token.
     */
    @NotNull(message = "SESSION_REFRESH_THRESHOLD must be provided")
    @jakarta.validation.constraints.DecimalMin(
            value = "0.0",
            inclusive = false,
            message = "SESSION_REFRESH_THRESHOLD must be greater than 0"
    )
    @jakarta.validation.constraints.DecimalMax(
            value = "1.0",
            inclusive = false,
            message = "SESSION_REFRESH_THRESHOLD must be less than 1"
    )
    private Double sessionRefreshThreshold;
}

