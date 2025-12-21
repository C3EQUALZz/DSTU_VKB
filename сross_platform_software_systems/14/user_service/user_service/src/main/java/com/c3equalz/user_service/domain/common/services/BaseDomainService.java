package com.c3equalz.user_service.domain.common.services;

import com.c3equalz.user_service.domain.common.BaseDomainEvent;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Deque;
import java.util.List;

/**
 * Base class for domain services that can record and manage domain events.
 * <p>
 * Provides functionality to record domain events, retrieve them, clear them,
 * and pull events (return a copy and clear the collection).
 */
public abstract class BaseDomainService {

    /**
     * Internal storage for domain events.
     * Uses ArrayDeque for efficient insertion and iteration.
     */
    private final Deque<BaseDomainEvent> events = new ArrayDeque<>();

    /**
     * Records a single domain event.
     *
     * @param event the domain event to record
     */
    protected void recordEvent(BaseDomainEvent event) {
        if (event == null) {
            throw new IllegalArgumentException("Event cannot be null");
        }
        events.add(event);
    }

    /**
     * Records multiple domain events.
     *
     * @param eventsToRecord the collection of domain events to record
     */
    protected void recordEvents(Collection<? extends BaseDomainEvent> eventsToRecord) {
        if (eventsToRecord == null) {
            throw new IllegalArgumentException("Events collection cannot be null");
        }
        events.addAll(eventsToRecord);
    }

    /**
     * Gets all recorded events as an unmodifiable collection.
     * The returned collection is a snapshot at the time of call.
     *
     * @return a list containing all recorded events
     */
    public List<BaseDomainEvent> getEvents() {
        return new ArrayList<>(events);
    }

    /**
     * Clears all recorded events.
     */
    public void clearEvents() {
        events.clear();
    }

    /**
     * Pulls all events: returns a copy of all events and clears the internal collection.
     * This is useful when you need to process events and ensure they are not
     * processed again.
     *
     * @return a list containing all recorded events (copy)
     */
    public List<BaseDomainEvent> pullEvents() {
        List<BaseDomainEvent> eventList = new ArrayList<>(events);
        events.clear();
        return eventList;
    }
}
