package com.c3equalz.user_service.application.common.ports;

import com.c3equalz.user_service.domain.user.values.UserID;
import reactor.core.publisher.Mono;

/**
 * Interface for getting current user identity.
 * For more information, see: <a href="https://t.me/advice17_chat/4929">Telegram Tishka17</a>
 */
public interface IdentityProvider {
    /**
     * Gets the current user ID from the security context.
     *
     * @return Mono containing the current user ID
     */
    Mono<UserID> getCurrentUserID();
}
