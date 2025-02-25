package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.Order;
import com.example.repairserviceapp.entities.OrderHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface OrdersRepo extends JpaRepository<Order, UUID> {
    @Modifying
    @Query(value = """
            INSERT INTO orders (order_code, equipment_code, client_code, master_code, order_status, order_date, order_components_code, sys_period)
            VALUES (:#{#orderHistory.id},:#{#equipmentCode}, :#{#clientCode}, :#{#masterCode}, :#{#statusCode}, :#{#orderHistory.date}, :#{#orderComponentsCode}, :#{#orderHistory.localDateRange})
            ON CONFLICT (order_code) DO UPDATE
            SET
                equipment_code = :#{#equipmentCode},
                client_code = :#{#clientCode},
                master_code = :#{#masterCode},
                order_status = :#{#statusCode},
                order_date = :#{#orderHistory.date},
                order_components_code = :#{#orderComponentsCode},
                sys_period = :#{#orderHistory.localDateRange}
            """, nativeQuery = true)
    void syncOrderFromHistory(
            @Param("orderHistory") OrderHistory orderHistory,
            @Param("clientCode") UUID clientCode,
            @Param("equipmentCode") UUID equipmentCode,
            @Param("masterCode") UUID masterCode,
            @Param("statusCode") UUID statusCode,
            @Param("orderComponentsCode") UUID orderComponentsCode
    );
}
