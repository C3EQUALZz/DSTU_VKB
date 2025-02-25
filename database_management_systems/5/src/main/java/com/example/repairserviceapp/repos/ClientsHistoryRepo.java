package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.ClientHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ClientsHistoryRepo extends JpaRepository<ClientHistory, UUID> {
    @Query(
            value = "SELECT * FROM clients_history WHERE client_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<ClientHistory> findByClientIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
