package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.PostHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

public interface PostsHistoryRepo extends JpaRepository<PostHistory, UUID> {
    @Query(
            value = "SELECT * FROM posts_history WHERE post_code = :id AND sys_period @> (:timestamp)::TIMESTAMPTZ",
            nativeQuery = true
    )
    Optional<PostHistory> findByPostIdAndTimestamp(
            @Param("id") UUID id,
            @Param("timestamp") OffsetDateTime timestamp
    );
}
