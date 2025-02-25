package com.example.repairserviceapp.services;

import com.example.repairserviceapp.entities.Order;
import com.example.repairserviceapp.entities.OrderHistory;
import com.example.repairserviceapp.exceptions.EntityNotFoundException;
import com.example.repairserviceapp.repos.OrdersHistoryRepo;
import com.example.repairserviceapp.repos.OrdersRepo;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Slf4j
@Service
@Transactional(readOnly = true)
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class OrdersService {

    private final OrdersRepo ordersRepo;
    private final OrdersHistoryRepo ordersHistoryRepo;

    public List<Order> readAll() {
        return ordersRepo.findAll();
    }

    public Order read(UUID id) {
        return ordersRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no order with this id"));
    }

    @Transactional
    public Order create(Order order) {
        order.setId(UUID.randomUUID());
        return ordersRepo.save(order);
    }

    @Transactional
    public Order update(UUID id, Order order) {
        ordersRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no order with this id"));
        order.setId(id);
        return ordersRepo.save(order);
    }

    @Transactional
    public Order delete(UUID id) {
        Order oldOrder = ordersRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no order with this id"));
        ordersRepo.deleteById(id);
        return oldOrder;
    }

    public List<OrderHistory> readAllHistory() {
        return ordersHistoryRepo.findAll();
    }

    @Transactional
    public Order restore(UUID orderId, OffsetDateTime timestamp) {
        OrderHistory orderHistory = ordersHistoryRepo
                .findByOrderIdAndTimestamp(orderId, timestamp)
                .orElseThrow(() -> new EntityNotFoundException(
                        "There is no order with this id " + orderId + " and timestamp " + timestamp
                ));

        ordersRepo.syncOrderFromHistory(
                orderHistory,
                orderHistory.getClientCode(),
                orderHistory.getEquipmentCode(),
                orderHistory.getMasterCode(),
                orderHistory.getStatusCode(),
                orderHistory.getOrderComponentsCode()
        );

        ordersHistoryRepo.delete(orderHistory);

        return ordersRepo.findById(orderId).orElseThrow(() -> new EntityNotFoundException("There is no order with this id"));
    }
}
