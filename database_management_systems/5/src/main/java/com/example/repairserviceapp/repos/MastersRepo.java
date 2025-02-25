package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.Master;
import com.example.repairserviceapp.entities.MasterHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface MastersRepo extends JpaRepository<Master, UUID> {
    @Modifying
    @Query(value = """
            INSERT INTO masters_list (master_code, name, surname, patronymic, phone_number, address, post_code, date_of_employment,sys_period)
            VALUES (:#{#masterHistory.id}, :#{#masterHistory.name}, :#{#masterHistory.surname}, :#{#masterHistory.patronymic}, :#{#masterHistory.phoneNumber}, :#{#masterHistory.address}, :#{#postId}, :#{#masterHistory.dateOfEmployment}, :#{#masterHistory.localDateRange})
            ON CONFLICT (master_code) DO UPDATE
            SET
                name = :#{#masterHistory.name},
                surname = :#{#masterHistory.surname},
                patronymic = :#{#masterHistory.patronymic},
                phone_number = :#{#masterHistory.phoneNumber},
                address = :#{#masterHistory.address},
                post_code = :#{#postId},
                date_of_employment = :#{#masterHistory.dateOfEmployment},
                sys_period = :#{#masterHistory.localDateRange}
            """, nativeQuery = true)
    void syncMasterFromHistory(
            @Param("masterHistory") MasterHistory masterHistory,
            @Param("postId") UUID postId
    );
}
