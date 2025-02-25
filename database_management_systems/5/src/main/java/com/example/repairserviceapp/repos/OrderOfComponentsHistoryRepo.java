package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.OrderOfComponentsHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface OrderOfComponentsHistoryRepo extends JpaRepository<OrderOfComponentsHistory, UUID> {
    @Query(
            value = "SELECT * FROM components_order_history WHERE co_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<OrderOfComponentsHistory> findByOrderOfComponentsIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
