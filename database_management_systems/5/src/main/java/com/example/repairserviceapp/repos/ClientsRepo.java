package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.Client;
import com.example.repairserviceapp.entities.ClientHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface ClientsRepo extends JpaRepository<Client, UUID> {
    Optional<Client> findByEmail(String email);

    @Modifying
    @Query(value = """
            INSERT INTO clients (client_code, name, surname, patronymic, phone_number, email, password, role, sys_period)
            VALUES (:#{#clientHistory.id}, :#{#clientHistory.name}, :#{#clientHistory.surname}, :#{#clientHistory.patronymic}, :#{#clientHistory.phoneNumber}, :#{#clientHistory.email}, :#{#clientHistory.password}, :#{#clientHistory.role}, :#{#clientHistory.localDateRange})
            ON CONFLICT (client_code) DO UPDATE
            SET
                name = :#{#clientHistory.name},
                surname = :#{#clientHistory.surname},
                patronymic = :#{#clientHistory.patronymic},
                phone_number = :#{#clientHistory.phoneNumber},
                email = :#{#clientHistory.email},
                password = :#{#clientHistory.password},
                role = :#{#clientHistory.role},
                sys_period = :#{#clientHistory.localDateRange}
            """, nativeQuery = true)
    void syncClientsFromHistory(@Param("clientHistory") ClientHistory clientHistory);
}
