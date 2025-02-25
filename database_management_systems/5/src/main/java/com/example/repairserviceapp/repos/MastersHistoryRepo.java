package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.MasterHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

public interface MastersHistoryRepo extends JpaRepository<MasterHistory, UUID> {
    @Query(
            value = "SELECT * FROM masters_list_history WHERE master_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<MasterHistory> findByMasterIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
