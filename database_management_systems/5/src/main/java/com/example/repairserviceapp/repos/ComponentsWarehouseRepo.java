package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.ComponentsWarehouse;
import com.example.repairserviceapp.entities.ComponentsWarehouseHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ComponentsWarehouseRepo extends JpaRepository<ComponentsWarehouse, UUID> {
    @Modifying
    @Query(value = """
            INSERT INTO components_warehouse (components_code, component_name, components_amount, unit_cost, sys_period)
            VALUES (:#{#componentsWarehouseHistory.id},:#{#componentsWarehouseHistory.componentName}, :#{#componentsWarehouseHistory.componentsAmount}, :#{#componentsWarehouseHistory.unitCost}, :#{#componentsWarehouseHistory.localDateRange})
            ON CONFLICT (components_code) DO UPDATE
            SET
                component_name = :#{#componentsWarehouseHistory.componentName},
                components_amount = :#{#componentsWarehouseHistory.componentsAmount},
                unit_cost = :#{#componentsWarehouseHistory.unitCost},
                sys_period = :#{#componentsWarehouseHistory.localDateRange}
            """, nativeQuery = true)
    void syncComponentWarehouseFromHistory(@Param("componentsWarehouseHistory") ComponentsWarehouseHistory componentsWarehouseHistory);
}
