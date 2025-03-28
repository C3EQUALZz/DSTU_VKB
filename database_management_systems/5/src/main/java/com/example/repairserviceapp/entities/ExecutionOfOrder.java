package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Entity
@Table(name = "order_executions")
@Getter
@Setter
@ToString
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class ExecutionOfOrder extends BaseExecutionOfOrder {
    @OneToMany(mappedBy="executionOfOrder")
    @ToString.Exclude
    private List<OrderOfComponents> ordersOfComponents;
}
