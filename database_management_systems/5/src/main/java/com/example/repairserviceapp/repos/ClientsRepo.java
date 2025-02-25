package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.Client;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface ClientsRepo extends JpaRepository<Client, UUID> {
    Optional<Client> findByEmail(String email);
}
