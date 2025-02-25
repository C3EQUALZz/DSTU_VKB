package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.OrderHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface OrdersHistoryRepo extends JpaRepository<OrderHistory, UUID> {
    @Query(
            value = "SELECT * FROM orders_history WHERE order_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<OrderHistory> findByOrderIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
