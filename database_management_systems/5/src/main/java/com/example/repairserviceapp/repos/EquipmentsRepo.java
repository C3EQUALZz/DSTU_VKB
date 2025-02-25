package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.Equipment;
import com.example.repairserviceapp.entities.EquipmentHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface EquipmentsRepo extends JpaRepository<Equipment, UUID> {

    @Modifying
    @Query(value = """
            INSERT INTO equipments (eq_code, eq_name, eq_serial_number, model, sys_period)
            VALUES (:#{#equipmentHistory.id},:#{#equipmentHistory.name}, :#{#equipmentHistory.serialNumber}, :#{#equipmentHistory.model}, :#{#equipmentHistory.localDateRange})
            ON CONFLICT (eq_code) DO UPDATE
            SET
                eq_name = :#{#equipmentHistory.name},
                eq_serial_number = :#{#equipmentHistory.serialNumber},
                model = :#{#equipmentHistory.model},
                sys_period = :#{#equipmentHistory.localDateRange}
            """, nativeQuery = true)
    void syncEquipmentsFromHistory(@Param("equipmentHistory") EquipmentHistory equipmentHistory);
}
