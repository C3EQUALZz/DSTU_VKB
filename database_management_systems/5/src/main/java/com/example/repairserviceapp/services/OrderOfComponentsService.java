package com.example.repairserviceapp.services;

import com.example.repairserviceapp.entities.OrderOfComponents;
import com.example.repairserviceapp.entities.OrderOfComponentsHistory;
import com.example.repairserviceapp.exceptions.EntityNotFoundException;
import com.example.repairserviceapp.repos.OrderOfComponentsHistoryRepo;
import com.example.repairserviceapp.repos.OrderOfComponentsRepo;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Service
@Transactional(readOnly = true)
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class OrderOfComponentsService {

    private final OrderOfComponentsRepo orderOfComponentsRepo;
    private final OrderOfComponentsHistoryRepo orderOfComponentsHistoryRepo;

    public List<OrderOfComponents> readAll() {
        return orderOfComponentsRepo.findAll();
    }

    public OrderOfComponents read(UUID id) {
        if (id == null) {
            return null;
        }
        return orderOfComponentsRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no OrderOfComponents with this id"));
    }

    @Transactional
    public OrderOfComponents create(OrderOfComponents orderOfComponents) {
        orderOfComponents.setId(UUID.randomUUID());
        return orderOfComponentsRepo.save(orderOfComponents);
    }

    @Transactional
    public OrderOfComponents update(UUID id, OrderOfComponents orderOfComponents) {
        orderOfComponentsRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no order of components with this id"));
        orderOfComponents.setId(id);
        return orderOfComponentsRepo.save(orderOfComponents);
    }

    @Transactional
    public OrderOfComponents delete(UUID id) {
        OrderOfComponents oldOrderOfComponents = orderOfComponentsRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no order of components with this id"));
        orderOfComponentsRepo.deleteById(id);
        return oldOrderOfComponents;
    }

    public List<OrderOfComponentsHistory> readAllHistory() {
        return orderOfComponentsHistoryRepo.findAll();
    }

    @Transactional
    public OrderOfComponentsHistory restore(UUID orderOfComponentId, OffsetDateTime timestamp) {

        OrderOfComponentsHistory historyOrder = orderOfComponentsHistoryRepo
                .findByOrderOfComponentsIdAndTimestamp(orderOfComponentId, timestamp)
                .orElseThrow(() -> new EntityNotFoundException(
                        "There is no order with this id " + orderOfComponentId + " and this timestamp " + timestamp
                ));

        return orderOfComponentsHistoryRepo.save(historyOrder);
    }
}
