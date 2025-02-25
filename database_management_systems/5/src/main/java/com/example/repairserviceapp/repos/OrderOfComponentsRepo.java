package com.example.repairserviceapp.repos;

import com.example.repairserviceapp.entities.OrderOfComponents;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface OrderOfComponentsRepo extends JpaRepository<OrderOfComponents, UUID> {
}
