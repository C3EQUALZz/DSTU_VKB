package com.c3equalz.user_service.infrastructure.auth.session;

import com.c3equalz.user_service.setup.config.security.AuthSettings;
import lombok.RequiredArgsConstructor;

import java.time.Duration;
import java.time.Instant;

@RequiredArgsConstructor
public class UtcAuthSessionTimer {
    private final AuthSettings authSettings;

    public Instant currentTime() {
        return Instant.now();
    }

    public Instant authSessionExpiration() {
        return currentTime().plus(authSettings.getSessionTtlMin());
    }

    public Instant refreshBiggerInterval() {
        Duration ttl = authSettings.getSessionTtlMin();
        double threshold = authSettings.getSessionRefreshThreshold();
        Duration interval = Duration.ofNanos((long) (ttl.toNanos() * threshold));
        return currentTime().plus(interval);
    }

    /**
     * Returns the duration threshold for triggering session refresh.
     * If remaining time until expiration is less than this, session should be refreshed.
     *
     * @return Duration representing the refresh trigger interval
     */
    public Duration refreshTriggerInterval() {
        Duration ttl = authSettings.getSessionTtlMin();
        double threshold = authSettings.getSessionRefreshThreshold();
        return Duration.ofNanos((long) (ttl.toNanos() * threshold));
    }
}
