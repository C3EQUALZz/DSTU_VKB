package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.EquipmentHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface EquipmentsHistoryRepo extends JpaRepository<EquipmentHistory, UUID> {
    @Query(
            value = "SELECT * FROM equipments_history WHERE eq_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<EquipmentHistory> findByEquipmentIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
