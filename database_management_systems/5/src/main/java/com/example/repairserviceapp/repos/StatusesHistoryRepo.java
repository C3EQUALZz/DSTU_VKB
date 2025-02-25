package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.StatusHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface StatusesHistoryRepo extends JpaRepository<StatusHistory, UUID> {
    @Query(
            value = "SELECT * FROM orders_statuses_history WHERE status_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<StatusHistory> findByStatusIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
