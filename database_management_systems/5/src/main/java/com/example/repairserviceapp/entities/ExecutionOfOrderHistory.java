package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "order_executions_history")
@Getter
@Setter
@ToString
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ExecutionOfOrderHistory extends BaseExecutionOfOrder {
    @OneToMany(mappedBy = "executionOfOrder")
    @ToString.Exclude
    private List<OrderOfComponentsHistory> ordersOfComponents;
}
