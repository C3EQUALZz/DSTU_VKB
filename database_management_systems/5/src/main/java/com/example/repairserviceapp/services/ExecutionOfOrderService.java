package com.example.repairserviceapp.services;

import com.example.repairserviceapp.entities.ExecutionOfOrder;
import com.example.repairserviceapp.entities.ExecutionOfOrderHistory;
import com.example.repairserviceapp.exceptions.EntityNotFoundException;
import com.example.repairserviceapp.repos.ExecutionOfOrderHistoryRepo;
import com.example.repairserviceapp.repos.ExecutionOfOrderRepo;
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
public class ExecutionOfOrderService {
    private ExecutionOfOrderRepo executionOfOrderRepo;
    private ExecutionOfOrderHistoryRepo executionOfOrderHistoryRepo;

    public List<ExecutionOfOrder> readAll() {
        return executionOfOrderRepo.findAll();
    }

    public ExecutionOfOrder read(UUID id) {
        return executionOfOrderRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no execution of order with this id"));
    }

    @Transactional
    public ExecutionOfOrder create(ExecutionOfOrder executionOfOrder) {
        executionOfOrder.setId(UUID.randomUUID());
        return executionOfOrderRepo.save(executionOfOrder);
    }

    @Transactional
    public ExecutionOfOrder update(UUID id, ExecutionOfOrder executionOfOrder) {
        executionOfOrderRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no execution of order with this id"));
        executionOfOrder.setId(id);
        return executionOfOrderRepo.save(executionOfOrder);
    }

    @Transactional
    public ExecutionOfOrder delete(UUID id) {
        ExecutionOfOrder oldExecutionOfOrder = executionOfOrderRepo.findById(id).orElseThrow(() -> new EntityNotFoundException("There is no execution of order with this id"));
        executionOfOrderRepo.deleteById(id);
        return oldExecutionOfOrder;
    }

    public List<ExecutionOfOrderHistory> readAllHistory() {
        return executionOfOrderHistoryRepo.findAll();
    }

    @Transactional
    public ExecutionOfOrderHistory restore(UUID orderId, OffsetDateTime timestamp) {

        ExecutionOfOrderHistory executionOfOrderHistory = executionOfOrderHistoryRepo
                .findByExecutionOfOrderIdAndTimestamp(orderId, timestamp)
                .orElseThrow(() -> new EntityNotFoundException(
                        "There is no order with this id " + orderId + " or timestamp " + timestamp));

        return executionOfOrderHistoryRepo.save(executionOfOrderHistory);
    }

}
