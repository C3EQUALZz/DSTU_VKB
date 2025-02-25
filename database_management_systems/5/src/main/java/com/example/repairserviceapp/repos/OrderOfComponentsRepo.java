package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.OrderOfComponents;
import com.example.repairserviceapp.entities.OrderOfComponentsHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface OrderOfComponentsRepo extends JpaRepository<OrderOfComponents, UUID> {
    @Modifying
    @Query(value = """
            INSERT INTO components_order (co_code, component_code, execution_code, sys_period)
            VALUES (:#{#orderOfComponentsHistory.id},:#{#orderOfComponentsHistory.componentCode}, :#{#orderOfComponentsHistory.executionCode}, :#{#orderOfComponentsHistory.localDateRange})
            ON CONFLICT (co_code) DO UPDATE
            SET
                component_code = :#{#componentCode},
                execution_code = :#{#executionCode},
                sys_period = :#{#orderOfComponentsHistory.localDateRange}
            """, nativeQuery = true)
    void syncOrderOfComponentsFromHistory(
            @Param("orderOfComponentsHistory") OrderOfComponentsHistory orderOfComponentsHistory,
            @Param("componentCode") UUID componentCode,
            @Param("executionCode") UUID executionCode
    );
}
