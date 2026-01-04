package com.c3equalz.user_service.application.common.ports;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;
import reactor.core.publisher.Mono;

import java.util.List;

/**
 * Interface for publishing domain events.
 * <p>
 * This interface allows publishing domain events to an event bus or message broker.
 */
public interface EventBus {

    /**
     * Publishes a list of domain events.
     *
     * @param events the list of domain events to publish
     * @return Mono that completes when all events are published
     */
    Mono<Void> publish(List<BaseDomainEvent> events);
}



