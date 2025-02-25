package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "order_executions")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Getter
@Setter
@ToString
public class ExecutionOfOrder extends BaseEntity {

    @Id
    @Column(name = "ex_code")
    private UUID id;

    @Column(name = "type_of_work")
    private String typeOfWork;

    @Column(name = "ex_cost")
    private BigDecimal exCost;

    @Column(name = "components_cost")
    private BigDecimal componentsCost;

    @Column(name = "ex_date")
    private LocalDate executionDate;

    @Column(name = "total_cost")
    private BigDecimal totalCost;

    @OneToMany(mappedBy="executionOfOrder")
    @ToString.Exclude
    private List<OrderOfComponents> ordersOfComponents;

}
