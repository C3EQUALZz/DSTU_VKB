package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.ExecutionOfOrderHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ExecutionOfOrderHistoryRepo extends JpaRepository<ExecutionOfOrderHistory, UUID> {
    @Query(
            value = "SELECT * FROM order_executions_history WHERE ex_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<ExecutionOfOrderHistory> findByExecutionOfOrderIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
