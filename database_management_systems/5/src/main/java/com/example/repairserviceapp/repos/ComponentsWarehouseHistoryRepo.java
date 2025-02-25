package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.ComponentsWarehouseHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ComponentsWarehouseHistoryRepo extends JpaRepository<ComponentsWarehouseHistory, UUID> {
    @Query(
            value = "SELECT * FROM components_warehouse_history WHERE components_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<ComponentsWarehouseHistory> findByComponentsWarehouseIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
